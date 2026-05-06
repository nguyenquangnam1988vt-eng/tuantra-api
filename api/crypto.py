import os
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY = os.getenv("GROUP_KEY", "0123456789abcdef0123456789abcdef").encode()

def encrypt(data: dict) -> str:
    iv = os.urandom(12)

    cipher = Cipher(
        algorithms.AES(KEY),
        modes.GCM(iv),
        backend=default_backend()
    )

    enc = cipher.encryptor()

    plaintext = json.dumps(data).encode()

    ciphertext = enc.update(plaintext) + enc.finalize()

    return base64.b64encode(iv + enc.tag + ciphertext).decode()


def decrypt(token: str) -> dict:
    raw = base64.b64decode(token)

    iv = raw[:12]
    tag = raw[12:28]
    ciphertext = raw[28:]

    cipher = Cipher(
        algorithms.AES(KEY),
        modes.GCM(iv, tag),
        backend=default_backend()
    )

    dec = cipher.decryptor()

    plaintext = dec.update(ciphertext) + dec.finalize()

    return json.loads(plaintext.decode())
