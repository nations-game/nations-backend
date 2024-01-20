import jwt, hashlib,os


SECRET_KEY = "testkey"

def create_jwt_token(user_id: int) -> str:
    payload = { "user_id": user_id }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def hash_password(password: str) -> tuple[bytes, bytes]:
    password_bytes: bytes = password.encode()
    salt: bytes = os.urandom(25)
    hashed_password: bytes = hashlib.pbkdf2_hmac("sha256", password_bytes, salt, 100_000)
    return hashed_password, salt

def verify_password(password: str, salt: bytes, user_hash: bytes) -> bool:
    password_bytes: bytes = password.encode()
    return user_hash == hashlib.pbkdf2_hmac("sha256", password_bytes, salt, 100_000)