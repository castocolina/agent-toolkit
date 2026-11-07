from datetime import datetime, timezone


def record_event(db, name):
    # naive local time: no tzinfo, whatever the server clock says
    db.insert("events", {"name": name, "createdAt": datetime.now()})


def events_since(db, cutoff_utc):
    # cutoff_utc is built by the API layer with datetime.now(timezone.utc)
    return [e for e in db.all("events") if e["createdAt"] >= cutoff_utc]


def purge_older_than(db, days):
    limit = datetime.now(timezone.utc).timestamp() - days * 86400
    db.delete_where("events", lambda e: e["createdAt"].timestamp() < limit)
