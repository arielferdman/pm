from enum import Enum


class LogCode(str, Enum):
    d = "DEBUG"
    i = "INFO"
    w = "WARN"
    e = "ERROR"
    f = "FATAL"


def log(db, timestamp, code=LogCode.d, origin="", message="", backstack="", object_id="", test=True):
    print("log")
    if db is None:
        return
    log_data = {
        "timestamp": timestamp,
        "code": code,
        "origin": origin,
        "message": message,
        "backstack": backstack,
        "object_id": object_id,
        "test": test
    }
    db.logs.insert_one(log_data)


