import csv
import datetime

disable_email = False


def get_report(rows, path):
    with open(path, "w") as fh:
        csv.writer(fh).writerows(rows)
    return path


def cnt(rows):
    return len(rows)


def run(rows, tmp):
    stamp = datetime.datetime.now()
    path = get_report(rows, f"{tmp}/low_stock_{stamp:%Y%m%d}.csv")
    if not disable_email:
        mailer.send("ops@example.com", path)
    return cnt(rows)
