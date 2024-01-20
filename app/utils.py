import hashlib
import os


def hash_password(password: str) -> tuple[bytes, bytes]:
    password_bytes: bytes = password.encode()
    salt: bytes = os.urandom(25)
    
    hashed_password: bytes = hashlib.pbkdf2_hmac("sha256", password_bytes, salt, 100_000)
    return hashed_password, salt

def check_password(password: str, salt: bytes, user_hash: bytes) -> bool:
    password_bytes: bytes = password.encode()
    
    return user_hash == hashlib.pbkdf2_hmac("sha256", password_bytes, salt, 100_000)

