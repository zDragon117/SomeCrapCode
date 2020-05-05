from datetime import date
from calendar import monthrange

ordinal_number = lambda n: "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n if n < 20 else n % 10, "th"))

def last_date_of_month():
    d = date.today()
    last_day = monthrange(d.year, d.month)[1]
    return date(d.year, d.month, last_day)