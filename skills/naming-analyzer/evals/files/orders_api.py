"""Order export endpoint consumed by the partner portal and the mobile app."""
from dataclasses import asdict, dataclass

EXPORT_FIELDS = ["ord_id", "usr_nm", "created"]


@dataclass
class OrderRow:
    ord_id: int
    usr_nm: str
    # Fixed by the payment provider's webhook schema v3: epoch seconds, UTC.
    created: int


def export_row(row: OrderRow) -> dict:
    data = asdict(row)
    return {key: data[key] for key in EXPORT_FIELDS}


def csv_header() -> str:
    return ",".join(EXPORT_FIELDS)


def handle_webhook(payload: dict) -> OrderRow:
    return OrderRow(
        ord_id=payload["ord_id"],
        usr_nm=payload["usr_nm"],
        created=payload["created"],
    )
