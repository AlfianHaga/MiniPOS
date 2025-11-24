from decimal import Decimal, ROUND_HALF_UP
from django import template

register = template.Library()


@register.filter(is_safe=True)
def idr(value, position="left"):
    """Format a number as Indonesian Rupiah.

    Usage in template: {{ value|idr }} or {{ value|idr:"right" }}
    Produces: 'Rp 1.234,00' by default or '1.234,00 Rp' when passed "right".
    """
    try:
        val = Decimal(value)
    except Exception:
        try:
            val = Decimal(str(value))
        except Exception:
            return value

    # round to 2 decimals
    q = val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    # get string with dot decimal separator
    s = f"{q:.2f}"
    integer, fraction = s.split(".")
    try:
        integer_part = int(integer)
        int_with_sep = "{:,}".format(integer_part).replace(",", ".")
    except Exception:
        int_with_sep = integer

    formatted = f"{int_with_sep},{fraction}"
    if str(position).lower() in ("right", "r"):
        return f"{formatted} Rp"
    return f"Rp {formatted}"
