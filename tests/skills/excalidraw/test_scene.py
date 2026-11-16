import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/excalidraw/scripts/scene.py"
FIXTURE = ROOT / "skills/excalidraw/evals/files/architecture.excalidraw.json"


def run(*args):
    r = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
    return r.returncode, (json.loads(r.stdout) if r.stdout.strip() else None), r.stderr


class SceneTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)

    def test_fixture_summary_and_check(self):
        code, out, _ = run("summary", FIXTURE)
        self.assertEqual(code, 0)
        self.assertEqual([s["label"] for s in out["shapes"]], ["Web Client", "API Service", "Postgres"])
        self.assertIn({"from": "Web Client", "to": "API Service", "label": "HTTPS"},
                      [{k: c[k] for k in ("from", "to", "label")} for c in out["connections"]])
        self.assertEqual(run("check", FIXTURE)[:2][0], 0)

    def test_new_scene_passes_check(self):
        spec = self.tmp / "spec.json"
        spec.write_text(json.dumps({"nodes": ["Request link", "Verify token", {"label": "Done", "shape": "ellipse"}],
                                    "edges": [["Request link", "Verify token"], ["Verify token", "Done", "ok"]]}))
        code, out, _ = run("new", spec, "-o", self.tmp / "flow.excalidraw")
        self.assertEqual((code, out["ok"]), (0, True))
        code, s, _ = run("summary", self.tmp / "flow.excalidraw")
        self.assertEqual([c["to"] for c in s["connections"]], ["Verify token", "Done"])

    def test_edit_add_connect_then_diff_shows_only_that(self):
        new = self.tmp / "new.json"
        code, out, _ = run("edit", FIXTURE, "-o", new, "--add-node", "Redis Cache", "--near", "api service",
                           "--connect", "API Service->Redis Cache")
        self.assertTrue(out["ok"])
        _, d, _ = run("diff", FIXTURE, new)
        self.assertEqual(d, {"added_shapes": ["Redis Cache"], "removed_shapes": [], "relabelled": [],
                             "added_connections": ["API Service -> Redis Cache"], "removed_connections": [],
                             "added_text": [], "removed_text": []})
        scene = json.loads(new.read_text())
        self.assertEqual(len({e["id"] for e in scene["elements"]}), len(scene["elements"]))

    def test_remove_cleans_bindings_and_relabel_sets_original_text(self):
        new = self.tmp / "new.json"
        code, out, err = run("edit", FIXTURE, "-o", new, "--remove", "API Service", "--relabel", "Postgres=Postgres 16")
        self.assertEqual(code, 0, err)
        _, d, _ = run("diff", FIXTURE, new)
        self.assertEqual(d["removed_shapes"], ["API Service"])
        self.assertEqual(d["relabelled"], ["Postgres -> Postgres 16"])
        self.assertEqual(len(d["removed_connections"]), 2)
        text = [e for e in json.loads(new.read_text())["elements"] if e.get("text") == "Postgres 16"][0]
        self.assertEqual(text["originalText"], "Postgres 16")

    def test_check_reports_one_sided_binding_and_duplicate_id(self):
        scene = json.loads(FIXTURE.read_text())
        arrow = next(e for e in scene["elements"] if e["type"] == "arrow")
        start = next(e for e in scene["elements"] if e["id"] == arrow["startBinding"]["elementId"])
        start["boundElements"] = [b for b in start["boundElements"] if b["id"] != arrow["id"]]
        scene["elements"].append(dict(scene["elements"][0]))
        bad = self.tmp / "bad.json"
        bad.write_text(json.dumps(scene))
        code, out, _ = run("check", bad)
        self.assertEqual(code, 1)
        self.assertTrue(any("does not list the arrow" in e for e in out["errors"]))
        self.assertTrue(any(e.startswith("duplicate id") for e in out["errors"]))

    def test_diff_treats_box_rename_as_relabel_not_edge_churn(self):
        files = ROOT / "skills/excalidraw/evals/files"
        _, d, _ = run("diff", files / "infra-v1.excalidraw", files / "infra-v2.excalidraw")
        self.assertEqual(d, {"added_shapes": [], "removed_shapes": [], "relabelled": ["Payments -> Payments API"],
                             "added_connections": ["Gateway -> Inventory"],
                             "removed_connections": ["Orders -> Inventory"], "added_text": [], "removed_text": []})
        _, s, _ = run("summary", files / "box.excalidraw")
        self.assertEqual([x["label"] for x in s["shapes"]], ["Billing"])

    def test_new_refuses_duplicate_node_label(self):
        spec = self.tmp / "dup.json"
        spec.write_text(json.dumps({"nodes": ["API", "Worker", "api"], "edges": [["Worker", "API"]]}))
        code, _, err = run("new", spec, "-o", self.tmp / "dup.excalidraw")
        self.assertEqual(code, 1)
        self.assertIn("duplicate node label", err)
        self.assertFalse((self.tmp / "dup.excalidraw").exists())

    def scene_copy(self, mutate, name="copy.json"):
        scene = json.loads(FIXTURE.read_text())
        mutate(scene)
        path = self.tmp / name
        path.write_text(json.dumps(scene))
        return path, scene

    def by_label(self, scene, label):
        cid = next(e["containerId"] for e in scene["elements"] if e.get("text") == label)
        return next(e for e in scene["elements"] if e["id"] == cid)

    def test_diff_keeps_parallel_arrow_multiplicity(self):
        new = self.tmp / "new.json"
        run("edit", FIXTURE, "-o", new, "--connect", "Web Client->API Service", "--label", "HTTPS")
        _, d, _ = run("diff", FIXTURE, new)
        self.assertEqual(d["added_connections"], ["Web Client -> API Service [HTTPS]"])
        _, d, _ = run("diff", new, FIXTURE)
        self.assertEqual(d["removed_connections"], ["Web Client -> API Service [HTTPS]"])

    def test_diff_strict_flags_changes_outside_the_allowlist(self):
        def mutate(s):
            self.by_label(s, "Postgres")["strokeColor"] = "#ff0000"
            s["appState"]["viewBackgroundColor"] = "#000000"
        copy, scene = self.scene_copy(mutate)
        pg = self.by_label(scene, "Postgres")["id"]
        code, d, _ = run("diff", FIXTURE, copy, "--strict")
        self.assertEqual(code, 1)
        self.assertFalse(d["preservation"]["ok"])
        self.assertIn(f"{pg} (Postgres) changed: strokeColor", d["preservation"]["violations"])
        self.assertIn("top-level appState.viewBackgroundColor changed", d["preservation"]["violations"])
        self.assertEqual(d["relabelled"], [])  # the label-level diff alone misses both changes
        copy2, scene2 = self.scene_copy(lambda s: self.by_label(s, "Postgres").update(strokeColor="#ff0000"), "c2.json")
        code, d, _ = run("diff", FIXTURE, copy2, "--strict", "--allow", pg)
        self.assertEqual((code, d["preservation"]), (0, {"ok": True, "violations": []}))

    def test_edit_leaves_untouched_elements_and_top_level_identical(self):
        new = self.tmp / "new.json"
        run("edit", FIXTURE, "-o", new, "--add-node", "Redis Cache", "--near", "API Service",
            "--connect", "API Service->Redis Cache")
        old, out = json.loads(FIXTURE.read_text()), json.loads(new.read_text())
        api = self.by_label(old, "API Service")["id"]
        after = {e["id"]: e for e in out["elements"]}
        for e in old["elements"]:
            if e["id"] != api:
                self.assertEqual(after[e["id"]], e)
        self.assertEqual({k: v for k, v in out.items() if k != "elements"},
                         {k: v for k, v in old.items() if k != "elements"})
        self.assertEqual(run("diff", FIXTURE, new, "--strict", "--allow", api)[0], 1)  # new ids not allowed
        created = [e["id"] for e in out["elements"] if e["id"] not in {x["id"] for x in old["elements"]}]
        allow = [arg for i in [api, *created] for arg in ("--allow", i)]
        code, d, _ = run("diff", FIXTURE, new, "--strict", *allow)
        self.assertEqual(code, 0, d)

    def endpoints(self, scene_path):
        scene = json.loads(Path(scene_path).read_text())
        by_id = {e["id"]: e for e in scene["elements"]}
        ar = next(e for e in scene["elements"] if e["type"] == "arrow")
        start = (ar["x"] + ar["points"][0][0], ar["y"] + ar["points"][0][1])
        return by_id[ar["startBinding"]["elementId"]], start, ar, by_id

    def test_arrow_starts_on_diamond_and_ellipse_outlines(self):
        for shape, metric in (("diamond", lambda dx, dy: abs(dx) + abs(dy)),
                              ("ellipse", lambda dx, dy: (dx * dx + dy * dy) ** 0.5)):
            spec = self.tmp / f"{shape}.json"
            spec.write_text(json.dumps({"nodes": [{"label": "Q", "shape": shape, "x": 0, "y": 0},
                                                  {"label": "Yes", "x": 280, "y": 140}], "edges": [["Q", "Yes"]]}))
            out = self.tmp / f"{shape}.excalidraw"
            self.assertEqual(run("new", spec, "-o", out)[0], 0)
            box, (px, py), _, _ = self.endpoints(out)
            dx = (px - box["x"] - box["width"] / 2) / (box["width"] / 2)
            dy = (py - box["y"] - box["height"] / 2) / (box["height"] / 2)
            self.assertAlmostEqual(metric(dx, dy), 1.0, places=6, msg=shape)

    def free_text(self, s, text, x=0, y=400, eid=None):
        s["elements"].append({"id": eid or f"note-{len(s['elements'])}", "type": "text", "x": x, "y": y,
                              "width": 100, "height": 25, "text": text, "originalText": text, "containerId": None,
                              "boundElements": None, "version": 1, "isDeleted": False})

    def test_strict_flags_unrequested_insertion_and_reordering(self):
        _, s, _ = run("summary", FIXTURE)
        pg = next(x["id"] for x in s["shapes"] if x["label"] == "Postgres")
        inserted, _ = self.scene_copy(lambda sc: self.free_text(sc, "stray", eid="stray1"), "ins.json")
        code, d, _ = run("diff", FIXTURE, inserted, "--strict", "--allow", pg)
        self.assertEqual(code, 1)
        self.assertIn("stray1 (stray) added", d["preservation"]["violations"])
        self.assertEqual(run("diff", FIXTURE, inserted, "--strict", "--allow", "stray1")[0], 0)
        reordered, _ = self.scene_copy(lambda sc: sc["elements"].reverse(), "rev.json")
        code, d, _ = run("diff", FIXTURE, reordered, "--strict")
        self.assertEqual(code, 1)
        self.assertIn("stacking order of untouched elements changed", d["preservation"]["violations"])

    def test_free_text_has_ids_resolves_by_id_and_shows_in_diff(self):
        def mutate(sc):
            self.free_text(sc, "TODO", eid="n1")
            self.free_text(sc, "TODO", eid="n2", y=450)
        copy, _ = self.scene_copy(mutate)
        _, s, _ = run("summary", copy)
        self.assertEqual(s["free_text"], [{"id": "n1", "text": "TODO"}, {"id": "n2", "text": "TODO"}])
        out = self.tmp / "out.json"
        self.assertIn("matches 2 elements", run("edit", copy, "-o", out, "--relabel", "TODO=Done")[2])
        code, _, err = run("edit", copy, "-o", out, "--relabel", "n2=Done")
        self.assertEqual(code, 0, err)
        _, d, _ = run("diff", copy, out)
        self.assertEqual(d["relabelled"], ["TODO -> Done"])
        _, d, _ = run("diff", FIXTURE, copy)
        self.assertEqual(d["added_text"], ["TODO", "TODO"])

    def test_self_loop_is_refused_before_writing(self):
        spec = self.tmp / "loop.json"
        spec.write_text(json.dumps({"nodes": ["Retry"], "edges": [["Retry", "Retry"]]}))
        code, _, err = run("new", spec, "-o", self.tmp / "loop.excalidraw")
        self.assertEqual(code, 1)
        self.assertIn("self-loop", err)
        self.assertFalse((self.tmp / "loop.excalidraw").exists())
        code, _, err = run("edit", FIXTURE, "-o", self.tmp / "x.json", "--connect", "Postgres->Postgres")
        self.assertEqual(code, 1)
        self.assertIn("self-loop", err)

    def test_new_refuses_to_overwrite_existing_out(self):
        spec = self.tmp / "s.json"
        spec.write_text(json.dumps({"nodes": ["A"]}))
        out = self.tmp / "exists.excalidraw"
        out.write_text("keep me")
        code, _, err = run("new", spec, "-o", out)
        self.assertEqual(code, 1)
        self.assertIn("already exists", err)
        self.assertEqual(out.read_text(), "keep me")

    def test_strict_allows_only_named_files_and_appstate_keys(self):
        def mutate(sc):
            sc["files"]["img1"] = {"id": "img1", "mimeType": "image/png", "dataURL": "data:image/png;base64,AA=="}
            sc["appState"]["viewBackgroundColor"] = "#000000"
        copy, _ = self.scene_copy(mutate)
        code, d, _ = run("diff", FIXTURE, copy, "--strict", "--allow-key", "files.img1")
        self.assertEqual(code, 1)
        self.assertEqual(d["preservation"]["violations"], ["top-level appState.viewBackgroundColor changed"])
        code, d, _ = run("diff", FIXTURE, copy, "--strict", "--allow-key", "files.img1",
                         "--allow-key", "appState.viewBackgroundColor")
        self.assertEqual(code, 0, d)

    def test_diff_strict_allowing_an_arrow_covers_its_label_text(self):
        new = self.tmp / "new.json"
        run("edit", FIXTURE, "-o", new, "--relabel", "HTTPS=HTTPS (TLS 1.3)")
        _, s, _ = run("summary", FIXTURE)
        arrow = next(c["id"] for c in s["connections"] if c["label"] == "HTTPS")
        self.assertEqual(run("diff", FIXTURE, new, "--strict")[0], 1)
        code, d, _ = run("diff", FIXTURE, new, "--strict", "--allow", arrow)
        self.assertEqual(code, 0, d)
        self.assertEqual((d["removed_connections"], d["added_connections"]),
                         (["Web Client -> API Service [HTTPS]"], ["Web Client -> API Service [HTTPS (TLS 1.3)]"]))

    def test_connect_refuses_rotated_shape(self):
        copy, _ = self.scene_copy(lambda s: self.by_label(s, "Postgres").update(angle=0.5))
        code, _, err = run("edit", copy, "-o", self.tmp / "x.json", "--connect", "Web Client->Postgres")
        self.assertEqual(code, 1)
        self.assertIn("rotated", err)
        self.assertFalse((self.tmp / "x.json").exists())

    def test_arrow_label_sits_on_the_arrow_pointing_left_and_up(self):
        spec = self.tmp / "s.json"
        spec.write_text(json.dumps({"nodes": [{"label": "A", "x": 400, "y": 300}, {"label": "B", "x": 0, "y": 0}],
                                    "edges": [["A", "B", "back"]]}))
        out = self.tmp / "s.excalidraw"
        self.assertEqual(run("new", spec, "-o", out)[0], 0)
        _, _, ar, by_id = self.endpoints(out)
        text = next(e for e in by_id.values() if e.get("containerId") == ar["id"])
        (x0, y0), (x1, y1) = ar["points"]
        self.assertAlmostEqual(text["x"] + text["width"] / 2, ar["x"] + (x0 + x1) / 2)
        self.assertAlmostEqual(text["y"] + text["height"] / 2, ar["y"] + (y0 + y1) / 2)

    def test_edit_refuses_when_original_already_has_dangling_binding(self):
        def mutate(s):
            arrow = next(e for e in s["elements"] if e["type"] == "arrow")
            arrow["endBinding"]["elementId"] = "gone"
        copy, _ = self.scene_copy(mutate)
        out = self.tmp / "out.json"
        code, _, err = run("edit", copy, "-o", out, "--relabel", "Postgres=Postgres 16")
        self.assertEqual(code, 1)
        self.assertIn("refusing to write an invalid scene", err)
        self.assertIn("gone is missing or deleted", err)
        self.assertFalse(out.exists())

    def test_add_node_may_reuse_an_arrow_label(self):
        code, out, err = run("edit", FIXTURE, "-o", self.tmp / "x.json", "--add-node", "HTTPS")
        self.assertEqual(code, 0, err)

    def test_edit_refuses_add_node_with_existing_label(self):
        code, _, err = run("edit", FIXTURE, "-o", self.tmp / "x.json", "--add-node", "api  service")
        self.assertEqual(code, 1)
        self.assertIn("duplicate node label", err)
        self.assertFalse((self.tmp / "x.json").exists())

    def test_edit_refuses_ambiguous_connect_target(self):
        twice = self.tmp / "twice.json"
        scene = json.loads(FIXTURE.read_text())
        for e in scene["elements"]:
            if e.get("text") == "Postgres":
                e["text"] = e["originalText"] = "Web Client"
        twice.write_text(json.dumps(scene))
        code, _, err = run("edit", twice, "-o", self.tmp / "x.json", "--connect", "Web Client->API Service")
        self.assertEqual(code, 1)
        self.assertIn("matches 2 elements", err)
        self.assertFalse((self.tmp / "x.json").exists())

    def test_edit_refuses_ambiguous_label_and_png(self):
        code, _, err = run("edit", FIXTURE, "-o", self.tmp / "x.json", "--relabel", "Nope=X")
        self.assertEqual(code, 1)
        self.assertIn("matches 0 elements", err)
        self.assertFalse((self.tmp / "x.json").exists())
        png = self.tmp / "d.excalidraw.png"
        png.write_bytes(b"\x89PNG")
        code, _, err = run("summary", png)
        self.assertEqual(code, 1)
        self.assertIn("save as .excalidraw", err)


if __name__ == "__main__":
    unittest.main()
