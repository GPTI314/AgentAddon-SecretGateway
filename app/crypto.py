import os, time, hmac, hashlib, secrets, base64, jwt
from .config import get_settings

settings = get_settings()

def _derive_key(master: str) -> bytes:
    return hashlib.sha256(master.encode()).digest()

def mint_ephemeral_secret(purpose: str, ttl: int | None = None) -> dict:
    ttl = ttl or settings.TOKEN_TTL_SECONDS
    exp = int(time.time()) + ttl
    payload = {"purpose": purpose, "exp": exp, "iat": int(time.time())}
    key = _derive_key(settings.MASTER_SECRET)
    token = jwt.encode(payload, key, algorithm=settings.SIGNING_ALG)
    return {"token": token, "expires": exp}

def verify_secret(token: str) -> dict:
    key = _derive_key(settings.MASTER_SECRET)
    try:
        data = jwt.decode(token, key, algorithms=[settings.SIGNING_ALG])
        return {"valid": True, "data": data}
    except Exception as e:  # broad catch for initial scaffold
        return {"valid": False, "error": str(e)}
