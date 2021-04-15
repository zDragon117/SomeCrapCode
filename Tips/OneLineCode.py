from datetime import date
from calendar import monthrange

ordinal_number = lambda n: "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n if n < 20 else n % 10, "th"))
grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
ANONYMOUS_DICT = {
    -1: 'All',
    0: 'Unknown',
    1: 'Something 1',
    2: 'Something 2',
}
# transform to dict with key and value to count or something to manipulate {-1: 'value to manipulate -1', 0: 'value to manipulate 0', 1: 'value to manipulate 1'}
b = {key: 'value to manipulate ' + str(key) for key, value in ANONYMOUS_DICT.items() if key != 2}
# transform back to np.array [['All', 'value to manipulate-1'], ['Unknown', 'value to manipulate0'], ['Something 1', 'value to manipulate1']]
c = [[ANONYMOUS_DICT[key], value] for key, value in b.items()]


def last_date_of_month():
    d = date.today()
    last_day = monthrange(d.year, d.month)[1]
    return date(d.year, d.month, last_day)
