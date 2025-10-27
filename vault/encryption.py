# vault/encryption.py
from cryptography.fernet import Fernet
from django.conf import settings

# Load Fernet instance with your key from settings.py
fernet = Fernet(settings.FERNET_KEY)

def encrypt_text(plain_text: str) -> str:
    """Encrypt a string and return base64-encoded ciphertext."""
    return fernet.encrypt(plain_text.encode()).decode()

def decrypt_text(cipher_text: str) -> str:
    """Decrypt a base64-encoded ciphertext."""
    return fernet.decrypt(cipher_text.encode()).decode()
