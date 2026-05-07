import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

GROUP_KEY = None

def get_group_key():
    key = os.getenv("GROUP_KEY")

    if not key:
        raise Exception("Missing GROUP_KEY in Vercel Environment Variables")

    key_bytes = key.encode()

    if len(key_bytes) != 32:
        raise Exception(f"GROUP_KEY must be 32 bytes, got {len(key_bytes)}")

    return key_bytes

GROUP_KEY = get_group_key()


def decrypt_message(data: str):
    raw = base64.b64decode(data)

    iv = raw[:12]
    tag = raw[12:28]
    ciphertext = raw[28:]

    cipher = Cipher(
        algorithms.AES(GROUP_KEY),
        modes.GCM(iv, tag),
        backend=default_backend()
    )

    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()
