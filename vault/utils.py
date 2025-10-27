# vault/utils.py
from cryptography.fernet import Fernet
from django.conf import settings
import os

# Use FERNET_KEY from settings (string). If not present, raise helpful error.
def get_fernet():
    key = getattr(settings, 'FERNET_KEY', None)
    if not key:
        # check env fallback
        raise RuntimeError("FERNET_KEY not set. Add FERNET_KEY to your .env or settings.")
    if isinstance(key, str):
        key = key.encode()
    return Fernet(key)

def encrypt_password(plain_text: str) -> str:
    f = get_fernet()
    token = f.encrypt(plain_text.encode())
    # store as utf-8 string
    return token.decode()

def decrypt_password(token_str: str) -> str:
    f = get_fernet()
    try:
        return f.decrypt(token_str.encode()).decode()
    except Exception:
        return ""
