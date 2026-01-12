import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16


def pad(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([pad_len]) * pad_len


def unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    return data[:-pad_len]


def encrypt(key: bytes, text: str) -> str:
    if len(key) != 32:
        raise ValueError("Anahtar 32 byte olmalı (AES-256)")

    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    padded = pad(text.encode("utf-8"))
    encrypted = cipher.encrypt(padded)

    return base64.b64encode(iv + encrypted).decode("utf-8")


def decrypt(key: bytes, payload: str) -> str:
    if len(key) != 32:
        raise ValueError("Anahtar 32 byte olmalı (AES-256)")

    raw = base64.b64decode(payload.encode("utf-8"))
    iv = raw[:16]
    ciphertext = raw[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)

    return unpad(decrypted).decode("utf-8")
