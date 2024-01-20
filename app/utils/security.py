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
    """
    Returns a hash and salt given a password

    Args:
        password `str`: The password to be salted and hashed.
    
    Returns:
        `tuple[bytes. bytes]`: A tuple containing the hashed password and the used salt
    """

    password_bytes: bytes = password.encode()
    salt: bytes = os.urandom(25)
    hashed_password: bytes = hashlib.pbkdf2_hmac("sha256", password_bytes, salt, 100_000)
    return hashed_password, salt

def verify_password(password: str, salt: bytes, user_hash: bytes) -> bool:
    """
    Verifies that the provided password is correct

    Args:
        password `str`: The password to be verified.
        salt `bytes`: The user's saved salt.
        user_hash `bytes`: The user's actual hash.

    Returns:
        `bool`: True if the provided password is correct, False otherwise.
    """

    password_bytes: bytes = password.encode()
    return user_hash == hashlib.pbkdf2_hmac("sha256", password_bytes, salt, 100_000)