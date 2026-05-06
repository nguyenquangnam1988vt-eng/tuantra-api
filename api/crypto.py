import os
import base64
import json
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

    encryptor = cipher.encryptor()

    plaintext = json.dumps(data).encode()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    result = iv + encryptor.tag + ciphertext

    return base64.b64encode(result).decode()


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

    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return json.loads(plaintext.decode())
