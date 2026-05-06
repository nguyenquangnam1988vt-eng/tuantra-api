import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

GROUP_KEY = os.getenv("GROUP_KEY").encode()

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
