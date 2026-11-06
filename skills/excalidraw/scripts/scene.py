#!/usr/bin/env python3
"""Read, check, compare, create and edit Excalidraw scenes without printing scene JSON.

Usage:
  scene.py summary FILE                  labels and connections, as JSON
  scene.py check FILE                    structural validation; exit 1 on errors
  scene.py diff OLD NEW [--strict [--allow ID ...] [--allow-key files.ID|appState.KEY ...]]
                                         label-level changes; --strict also fails (exit 1) on any
                                         added, removed, changed or reordered element outside the
                                         allowed ids, or any top-level change outside the allowed keys
  scene.py new SPEC -o OUT               build a scene from {"nodes": [...], "edges": [...]}
  scene.py edit FILE -o OUT [ops...]     --add-node LABEL [--near LABEL]
                                         --connect "A->B" [--label TEXT]
                                         --relabel "OLD=NEW"   --remove LABEL
Elements are addressed by label (case- and whitespace-insensitive) or by id.
All output is JSON on stdout; errors go to stderr with exit 1 (2 for bad usage).
"""
import argparse
import copy
import json
import random
import secrets
import sys
import time
from collections import Counter
from pathlib import Path

SHAPES = {"rectangle", "ellipse", "diamond"}
TOUCHED = set()  # ids edit() changed or removed; everything else must survive byte-for-byte
W, H, GAP_X, GAP_Y = 180, 80, 100, 60


class SceneError(Exception):
    pass


def load(path):
    p = Path(path)
    if p.suffix.lower() in {".png", ".svg"} or p.name.endswith(".excalidraw.md"):
        raise SceneError(f"{p.name}: embedded scenes are not edited here; open it in Excalidraw and save as .excalidraw")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise SceneError(f"{p.name}: not readable JSON: {e}") from e
    if not isinstance(data, dict) or not isinstance(data.get("elements"), list):
        raise SceneError(f"{p.name}: no top-level 'elements' array; not an Excalidraw scene")
    return data


def live(scene):
    return [e for e in scene["elements"] if isinstance(e, dict) and not e.get("isDeleted")]


def norm(s):
    return " ".join(str(s).split()).casefold()


def labels(scene):
    """Map container id -> bound text, for every live text element with a containerId."""
    return {e["containerId"]: e.get("text", "") for e in live(scene)
            if e.get("type") == "text" and e.get("containerId")}


def find(scene, key):
    els, lab = live(scene), labels(scene)
    if any(e.get("id") == key for e in els):
        return next(e for e in els if e.get("id") == key)
    hits = [e for e in els if e.get("type") != "text" and norm(lab.get(e.get("id"), "")) == norm(key)]
    hits += [e for e in els if e.get("type") == "text" and not e.get("containerId") and norm(e.get("text", "")) == norm(key)]
    if len(hits) != 1:
        raise SceneError(f"label {key!r} matches {len(hits)} elements; use an id from 'summary'")
    return hits[0]


def summary(scene):
    els, lab = live(scene), labels(scene)
    name = {e["id"]: lab.get(e["id"]) or e.get("text") or e["id"] for e in els if "id" in e}
    end = lambda b: name.get((b or {}).get("elementId"), "(unbound)")
    return {
        "shapes": [{"id": e["id"], "type": e["type"], "label": lab.get(e["id"], "")}
                   for e in els if e.get("type") in SHAPES | {"image", "frame"}],
        "connections": [{"id": e["id"], "from": end(e.get("startBinding")), "to": end(e.get("endBinding")),
                         "label": lab.get(e["id"], "")} for e in els if e.get("type") == "arrow"],
        "free_text": [{"id": e["id"], "text": e.get("text", "")} for e in els
                      if e.get("type") == "text" and not e.get("containerId")],
        "deleted_skipped": len(scene["elements"]) - len(els),
    }


def check(scene):
    errors, ids = [], {}
    for i, e in enumerate(scene["elements"]):
        if not isinstance(e, dict) or not e.get("id") or not e.get("type"):
            errors.append(f"element #{i} has no id or type")
            continue
        ids.setdefault(e["id"], []).append(e)
    errors += [f"duplicate id {k} ({len(v)} elements)" for k, v in ids.items() if len(v) > 1]
    by_id = {e["id"]: e for e in live(scene) if e.get("id")}
    files = scene.get("files") or {}
    for e in by_id.values():
        eid = e["id"]
        if e.get("containerId"):
            c = by_id.get(e["containerId"])
            if not c:
                errors.append(f"text {eid} containerId {e['containerId']} is missing or deleted")
            elif not any(b.get("id") == eid for b in c.get("boundElements") or []):
                errors.append(f"text {eid} -> container {c['id']} is not listed in its boundElements")
        for side in ("startBinding", "endBinding"):
            target = (e.get(side) or {}).get("elementId")
            if target is None:
                continue
            t = by_id.get(target)
            if not t:
                errors.append(f"arrow {eid} {side} {target} is missing or deleted")
            elif not any(b.get("id") == eid for b in t.get("boundElements") or []):
                errors.append(f"arrow {eid} {side} {target} does not list the arrow in boundElements")
        for b in e.get("boundElements") or []:
            o = by_id.get(b.get("id"))
            back = o and (o.get("containerId") == eid or eid in {(o.get(s) or {}).get("elementId")
                                                                 for s in ("startBinding", "endBinding")})
            if not back:
                errors.append(f"{eid} boundElements lists {b.get('id')}, which does not point back")
        if e.get("frameId") and e["frameId"] not in by_id:
            errors.append(f"{eid} frameId {e['frameId']} is missing or deleted")
        if e.get("type") == "image" and e.get("fileId") not in files:
            errors.append(f"image {eid} fileId {e.get('fileId')} has no entry in 'files'")
    if scene.get("type") != "excalidraw":
        errors.append("top-level 'type' is not 'excalidraw'")
    return {"ok": not errors, "elements": len(by_id), "errors": errors}


def diff(old, new):
    a, b = summary(old), summary(new)
    nodes = lambda s: {x["id"]: x["label"] for x in s["shapes"]}
    texts = lambda s: {x["id"]: x["text"] for x in s["free_text"]}
    na, nb, (ka, ea), (kb, eb) = nodes(a), nodes(b), edges(old, a), edges(new, b)
    ta, tb = texts(a), texts(b)
    both = {**na, **ta}, {**nb, **tb}
    return {
        "added_shapes": sorted(nb[k] or k for k in nb.keys() - na.keys()),
        "removed_shapes": sorted(na[k] or k for k in na.keys() - nb.keys()),
        "relabelled": sorted(f"{both[0][k]} -> {both[1][k]}" for k in both[0].keys() & both[1].keys()
                             if both[0][k] != both[1][k]),
        "added_connections": sorted(eb[k] for k in (Counter(kb) - Counter(ka)).elements()),
        "removed_connections": sorted(ea[k] for k in (Counter(ka) - Counter(kb)).elements()),
        "added_text": sorted(tb[k] for k in tb.keys() - ta.keys()),
        "removed_text": sorted(ta[k] for k in ta.keys() - tb.keys()),
    }


def preservation(old, new, allow, allow_keys=()):
    """Outside `allow` ids (each covering its bound text), nothing may be added, removed, changed or reordered;
    top-level data must match except `files.<id>` / `appState.<key>` entries named in `allow_keys`."""
    olds, news = [e for e in old["elements"] if isinstance(e, dict)], [e for e in new["elements"] if isinstance(e, dict)]
    allow = set(allow) | {e.get("id") for e in olds + news if e.get("containerId") in allow}
    bad = []
    for k in sorted((old.keys() | new.keys()) - {"elements"}):
        o, n = old.get(k), new.get(k)
        if k in ("files", "appState") and isinstance(o, dict) and isinstance(n, dict):
            bad += [f"top-level {k}.{s} changed" for s in sorted(o.keys() | n.keys())
                    if o.get(s) != n.get(s) and f"{k}.{s}" not in allow_keys]
        elif o != n:
            bad.append(f"top-level {k} changed")
    before, after, lab = {e.get("id") for e in olds}, {e.get("id"): e for e in news}, labels(new)
    bad += [f"{e.get('id')} ({e.get('text') or lab.get(e.get('id')) or e.get('type')}) added" for e in news
            if e.get("id") not in before and e.get("id") not in allow]
    keep = lambda els: [e.get("id") for e in els if e.get("id") in before and e.get("id") in after and e.get("id") not in allow]
    if keep(olds) != keep(news):
        bad.append("stacking order of untouched elements changed")
    lab = labels(old)
    for e in olds:
        eid = e.get("id")
        if eid in allow:
            continue
        name = f"{eid} ({lab.get(eid) or e.get('text') or e.get('type')})"
        if eid not in after:
            bad.append(f"{name} removed")
        elif after[eid] != e:
            bad.append(f"{name} changed: " + ", ".join(sorted(k for k in e.keys() | after[eid].keys()
                                                               if e.get(k) != after[eid].get(k))))
    return {"ok": not bad, "violations": bad}


def edges(scene, s):
    """(one key per arrow, so parallel arrows count; display text by key). Keys are (start id, end id, label),
    so renaming a box is a relabel, not a removed and an added edge."""
    ends = {e["id"]: tuple((e.get(k) or {}).get("elementId") for k in ("startBinding", "endBinding"))
            for e in live(scene) if e.get("type") == "arrow"}
    keys = [(*ends[c["id"]], c["label"]) for c in s["connections"]]
    return keys, {k: f"{c['from']} -> {c['to']}" + (f" [{c['label']}]" if c["label"] else "")
                  for k, c in zip(keys, s["connections"])}


# ---- element builders: every field the editor writes, so a fresh scene opens without repair

def base(kind, x, y, w, h, **extra):
    TOUCHED.add(eid := secrets.token_urlsafe(15))  # created ids are part of the request
    return {"id": eid, "type": kind, "x": x, "y": y, "width": w, "height": h,
            "angle": 0, "strokeColor": "#1e1e1e", "backgroundColor": "transparent", "fillStyle": "solid",
            "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [],
            "frameId": None, "roundness": None, "seed": random.randint(1, 2**31 - 1), "version": 1,
            "versionNonce": random.randint(1, 2**31 - 1), "isDeleted": False, "boundElements": [],
            "updated": int(time.time() * 1000), "link": None, "locked": False, **extra}


def text_for(container, text):
    lines = text.split("\n")
    w, h = max(len(l) for l in lines) * 11, len(lines) * 25
    if container["type"] == "arrow":  # points may be negative, so width/height do not locate the line
        pts = container["points"]
        (mx, my) = pts[len(pts) // 2] if len(pts) % 2 else [(a + b) / 2 for a, b in zip(*pts[len(pts) // 2 - 1:][:2])]
        cx, cy = container["x"] + mx, container["y"] + my
    else:
        cx, cy = container["x"] + container["width"] / 2, container["y"] + container["height"] / 2
    t = base("text", cx - w / 2, cy - h / 2, w, h, text=text, originalText=text, fontSize=20, fontFamily=1,
             textAlign="center", verticalAlign="middle", containerId=container["id"], lineHeight=1.25,
             autoResize=True, boundElements=None)
    container["boundElements"].append({"type": "text", "id": t["id"]})
    return t


def node(label, x, y, kind="rectangle"):
    box = base(kind, x, y, W, H, roundness={"type": 3} if kind == "rectangle" else None)
    return [box, text_for(box, label)]


def edge_point(box, toward):
    """Where the line from the shape's centre toward a point crosses its outline (unrotated shapes only)."""
    cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    dx, dy = toward[0] - cx, toward[1] - cy
    if dx == dy == 0:
        return cx, cy
    u, v = abs(dx) / (box["width"] / 2), abs(dy) / (box["height"] / 2)  # direction in half-size units
    s = {"ellipse": 1 / (u * u + v * v) ** 0.5, "diamond": 1 / (u + v)}.get(box["type"], 1 / max(u, v))
    return cx + dx * s, cy + dy * s


def arrow(a, b, label=None):
    if a is b:
        raise SceneError(f"self-loop on {a['id']}: no straight arrow can show it; use the worker route")
    if a.get("angle") or b.get("angle"):
        raise SceneError("cannot connect a rotated shape exactly; use the worker route")
    ca = (a["x"] + a["width"] / 2, a["y"] + a["height"] / 2)
    cb = (b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
    (x1, y1), (x2, y2) = edge_point(a, cb), edge_point(b, ca)
    ar = base("arrow", x1, y1, abs(x2 - x1), abs(y2 - y1), roundness={"type": 2}, points=[[0, 0], [x2 - x1, y2 - y1]],
              lastCommittedPoint=None, startArrowhead=None, endArrowhead="arrow", elbowed=False,
              startBinding={"elementId": a["id"], "focus": 0, "gap": 1},
              endBinding={"elementId": b["id"], "focus": 0, "gap": 1})
    for t in (a, b):
        t.setdefault("boundElements", [])
        t["boundElements"] = (t["boundElements"] or []) + [{"type": "arrow", "id": ar["id"]}]
        touch(t)
    return [ar] + ([text_for(ar, label)] if label else [])


def touch(e):
    TOUCHED.add(e["id"])
    e["version"] = e.get("version", 0) + 1
    e["versionNonce"] = random.randint(1, 2**31 - 1)
    e["updated"] = int(time.time() * 1000)


def new_scene(spec):
    scene = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com", "elements": [],
             "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"}, "files": {}}
    boxes = {}
    for i, n in enumerate(spec.get("nodes", [])):
        n = {"label": n} if isinstance(n, str) else n
        if norm(n["label"]) in boxes:
            raise SceneError(f"duplicate node label {n['label']!r}: edges resolve nodes by label, so labels must be unique")
        els = node(n["label"], n.get("x", i * (W + GAP_X)), n.get("y", 0), n.get("shape", "rectangle"))
        boxes[norm(n["label"])] = els[0]
        scene["elements"] += els
    for e in spec.get("edges", []):
        src, dst, lab = (e + [None])[:3] if isinstance(e, list) else (e["from"], e["to"], e.get("label"))
        try:
            scene["elements"] += arrow(boxes[norm(src)], boxes[norm(dst)], lab)
        except KeyError as k:
            raise SceneError(f"edge {src!r}->{dst!r}: unknown node {k}") from None
    return scene


def free_spot(scene, x, y):
    def overlaps(px, py):
        return any(px < e["x"] + e.get("width", 0) and e["x"] < px + W and py < e["y"] + e.get("height", 0)
                   and e["y"] < py + H for e in live(scene) if e.get("type") in SHAPES)
    while overlaps(x, y):
        y += H + GAP_Y
    return x, y


def edit(scene, args):
    els = scene["elements"]
    for key in args.remove:
        target = find(scene, key)
        doomed = {target["id"]} | {b["id"] for b in target.get("boundElements") or [] if b.get("type") == "text"}
        doomed |= {e["id"] for e in live(scene) if e.get("type") == "arrow" and target["id"] in
                   {(e.get(s) or {}).get("elementId") for s in ("startBinding", "endBinding")}}
        doomed |= {e["id"] for e in live(scene) if e.get("containerId") in doomed}  # arrow labels
        TOUCHED.update(doomed)
        scene["elements"] = els = [e for e in els if e.get("id") not in doomed]
        for e in live(scene):
            kept = [b for b in e.get("boundElements") or [] if b.get("id") not in doomed]
            if kept != (e.get("boundElements") or []):
                e["boundElements"] = kept
                touch(e)
    for pair in args.relabel:
        old, _, new = pair.partition("=")
        target = find(scene, old)
        txt = next((e for e in live(scene) if e.get("containerId") == target["id"]), None) \
            if target.get("type") != "text" else target
        if txt is None:
            raise SceneError(f"{old!r} has no bound text to relabel")
        txt["text"] = txt["originalText"] = new  # the editor re-wraps from originalText
        touch(txt)
    for label in args.add_node:
        shape_ids = {e["id"] for e in live(scene) if e.get("type") != "arrow"}
        if norm(label) in {norm(v) for k, v in labels(scene).items() if k in shape_ids}:
            raise SceneError(f"duplicate node label {label!r}: an existing element already has it; pick a unique label")
        anchor = find(scene, args.near) if args.near else None
        x, y = (anchor["x"] + anchor["width"] + GAP_X, anchor["y"]) if anchor else (0, 0)
        els += node(label, *free_spot(scene, x, y))
    for pair in args.connect:
        src, _, dst = pair.partition("->")
        if not dst:
            raise SceneError(f"--connect {pair!r}: expected 'A->B'")
        els += arrow(find(scene, src.strip()), find(scene, dst.strip()), args.label)
    return scene


def write(scene, out, original=None):
    result = check(scene)
    if not result["ok"]:
        raise SceneError("refusing to write an invalid scene: " + "; ".join(result["errors"]))
    kept = preservation(original, scene, TOUCHED) if original is not None else {"ok": True}
    if not kept["ok"]:
        raise SceneError("refusing to write: edit changed elements outside the request: " + "; ".join(kept["violations"]))
    tmp = Path(str(out) + ".tmp")
    tmp.write_text(json.dumps(scene, indent=2) + "\n", encoding="utf-8")
    tmp.replace(out)
    return {"written": str(out), **result}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("summary", "check"):
        sub.add_parser(name).add_argument("file")
    d = sub.add_parser("diff")
    d.add_argument("old")
    d.add_argument("new")
    d.add_argument("--strict", action="store_true")
    d.add_argument("--allow", action="append", default=[])
    d.add_argument("--allow-key", action="append", default=[])
    n = sub.add_parser("new")
    n.add_argument("spec")
    n.add_argument("-o", "--out", required=True)
    e = sub.add_parser("edit")
    e.add_argument("file")
    e.add_argument("-o", "--out", required=True)
    e.add_argument("--add-node", action="append", default=[])
    e.add_argument("--near")
    e.add_argument("--connect", action="append", default=[])
    e.add_argument("--label")
    e.add_argument("--relabel", action="append", default=[])
    e.add_argument("--remove", action="append", default=[])
    a = p.parse_args(argv)
    try:
        if a.cmd == "summary":
            res = summary(load(a.file))
        elif a.cmd == "check":
            res = check(load(a.file))
        elif a.cmd == "diff":
            old, new = load(a.old), load(a.new)
            res = diff(old, new)
            if a.strict:
                res["preservation"] = preservation(old, new, set(a.allow), set(a.allow_key))
                res["ok"] = res["preservation"]["ok"]
        elif a.cmd == "new":
            if Path(a.out).exists():
                raise SceneError(f"{a.out} already exists; write to a new name and diff, or ask before replacing it")
            res = write(new_scene(json.loads(Path(a.spec).read_text(encoding="utf-8"))), a.out)
        else:
            original = load(a.file)
            res = write(edit(copy.deepcopy(original), a), a.out, original)
    except (SceneError, OSError, ValueError) as err:
        print(f"scene.py: {err}", file=sys.stderr)
        return 1
    print(json.dumps(res, indent=2))
    return 0 if res.get("ok", True) else 1


if __name__ == "__main__":
    sys.exit(main())
