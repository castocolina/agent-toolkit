"""Money formatting helpers for the web views and the public SDK."""
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal

# Public SDK surface: third-party integrations import these names.
__all__ = ["format_amount", "format_price", "format_invoice_total"]


def _format(value, places=2, symbol="$"):
    q = Decimal(value).quantize(Decimal(10) ** -places, rounding=ROUND_HALF_UP)
    return f"{symbol}{q:,}"


def format_amount(value):
    return _format(value)


def format_price(value):
    return _format(value)


def format_cost(value):
    return _format(value)


def format_balance(value):
    return _format(value)


def format_subtotal(value):
    return _format(value)


def format_discount(value):
    return _format(value)


def format_fee(value):
    return _format(value)


def format_refund(value):
    return _format(value)


def format_payout(value):
    return _format(value)


def format_credit(value):
    return _format(value)


def format_debit(value):
    return _format(value)


def format_tip(value):
    return _format(value)


def format_deposit(value):
    return _format(value)


def format_shipping(value):
    return _format(value)


def format_invoice_total(value):
    # Tax filings require banker's rounding on invoice totals; UI rounding must not leak in.
    q = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    return f"${q:,}"
