import json
import os
import hashlib
import uuid

# ───────── CONFIG ─────────
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")


# ───────── HELPERS ─────────
def ensure_files():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)


def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ───────── REGISTER ─────────
def register(username: str, password: str) -> dict:
    ensure_files()

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    if username in users:
        return {
            "ok": False,
            "error": "Bu kullanıcı adı zaten kayıtlı"
        }

    user_id = uuid.uuid4().hex[:8]

    users[username] = {
        "id": user_id,
        "password": hash_pw(password)
    }

    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

    return {
        "ok": True,
        "id": user_id,
        "username": username
    }


# ───────── LOGIN ─────────
def login(username: str, password: str) -> dict:
    ensure_files()

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    if username not in users:
        return {
            "ok": False,
            "error": "Kullanıcı bulunamadı"
        }

    if users[username]["password"] != hash_pw(password):
        return {
            "ok": False,
            "error": "Parola yanlış"
        }

    return {
        "ok": True,
        "id": users[username]["id"],
        "username": username
    }
