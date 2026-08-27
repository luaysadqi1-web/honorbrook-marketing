"""Queue and log storage for the Honorbrook social routine. Stdlib only."""

import csv
import datetime
import json
import os
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE_DIR = os.path.join(ROOT, "queue")
LOG_PATH = os.path.join(ROOT, "logs", "posted-log.csv")

LOG_FIELDS = [
    "timestamp", "date", "platform", "pillar", "status",
    "post_id", "chars", "blocks", "text",
]


def load_dotenv(path=None):
    """Read .env into os.environ. Values already set in the environment win."""
    path = path or os.path.join(ROOT, ".env")
    if not os.path.exists(path):
        return False
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val
    return True


def queue_path(date_str):
    return os.path.join(QUEUE_DIR, "%s.json" % date_str)


def load_queue(date_str):
    path = queue_path(date_str)
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        return json.load(fh)


def save_queue(date_str, data):
    os.makedirs(QUEUE_DIR, exist_ok=True)
    with open(queue_path(date_str), "w") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def new_item(platform, pillar, text, note=""):
    return {
        "id": uuid.uuid4().hex[:10],
        "platform": platform,
        "pillar": pillar,
        "text": text,
        "note": note,
        "status": "pending",
        "post_id": None,
        "blocks": [],
    }


def append_log(row):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=LOG_FIELDS, extrasaction="ignore")
        if not exists:
            w.writeheader()
        w.writerow(row)


def today_str():
    return datetime.date.today().isoformat()
