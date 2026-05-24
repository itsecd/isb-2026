import hmac
import hashlib

def create_hmac(key: bytes, text: bytes) -> str:
    hmac_hash = hmac.new(key, text, hashlib.sha256).hexdigest()
    return hmac_hash

def verify_hmac(key:bytes, text: bytes, hmac_hash: str) -> bool:
    true_hmac = create_hmac(key, text)
    return hmac.compare_digest(true_hmac, hmac_hash)