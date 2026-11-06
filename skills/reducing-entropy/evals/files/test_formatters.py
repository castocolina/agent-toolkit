from billing.formatters import format_amount, format_invoice_total, format_price


def test_amount_rounds_half_up():
    assert format_amount("2.345") == "$2.35"


def test_price_matches_amount():
    assert format_price("1999.5") == "$1,999.50"


def test_invoice_total_uses_bankers_rounding():
    assert format_invoice_total("2.345") == "$2.34"
