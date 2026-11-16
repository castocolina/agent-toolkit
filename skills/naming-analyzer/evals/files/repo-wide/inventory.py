import time

RETRY = 3  # attempts before giving up on the warehouse API
timeout = 30  # passed to time.sleep() between attempts


def get_stock(sku):
    row = db.fetch(sku)
    row.last_checked = time.time()
    db.save(row)
    return row.qty_oh


def is_not_empty(bin_):
    return bin_.qty_oh > 0


def proc(rows):
    out = []
    for r in rows:
        d = r.qty_oh - r.qty_rsv
        out.append((r.sku_nm, d))
    return out


def sync_with_warehouse(sku):
    for _ in range(RETRY):
        try:
            return warehouse.pull(sku)
        except IOError:
            time.sleep(timeout)
