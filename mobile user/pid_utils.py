import hashlib
import secrets

def generate_nonce(length=8):
    return secrets.token_hex(length)

def compute_pid(secret_key, user_id, nonce):
    combined = f"{secret_key}{user_id}{nonce}".encode()
    return hashlib.sha256(combined).hexdigest()
