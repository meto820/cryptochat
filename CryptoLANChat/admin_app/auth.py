import json
import os
import hashlib

# Admin bilgilerinin tutulacağı dosya
ADMIN_FILE = os.path.join("data", "admin.json")


def _hash_password(password: str) -> str:
    """
    Parolayı SHA-256 ile hashler
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def check_or_create_admin(password: str) -> bool:
    """
    - admin.json yoksa: verilen parola ile admin oluşturur
    - varsa: parolayı doğrular
    """
    # data klasörü yoksa oluştur
    os.makedirs("data", exist_ok=True)

    # İlk kurulum
    if not os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {"password_hash": _hash_password(password)},
                f,
                indent=2
            )
        return True

    # Var olan admin doğrulama
    with open(ADMIN_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("password_hash") == _hash_password(password)
