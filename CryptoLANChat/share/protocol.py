import uuid, time

def build_message(username: str, encrypted_payload: str) -> dict:
    return {
        "type": "msg",
        "id": str(uuid.uuid4()),
        "from": username,
        "ts": int(time.time()),
        "payload": encrypted_payload
    }

def build_delete(message_id: str, username: str) -> dict:
    return {
        "type": "delete",
        "message_id": message_id,
        "by": username
    }
