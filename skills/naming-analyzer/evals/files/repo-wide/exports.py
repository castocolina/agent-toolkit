from dataclasses import dataclass

# Partner feed: the retailer's importer reads these CSV headers by name.
EXPORT_COLUMNS = ["sku_nm", "qty_oh"]


@dataclass
class StockRow:
    sku_nm: str
    qty_oh: int
    qty_rsv: int = 0


def to_feed(rows):
    return [{key: getattr(row, key) for key in EXPORT_COLUMNS} for row in rows]
