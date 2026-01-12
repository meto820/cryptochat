import json

LOG = "logs/messages.log"

def save(msg: dict):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(msg) + "\n")
