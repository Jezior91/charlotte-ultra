#!/usr/bin/env python3
"""
KOMBINATOR — MODUL 3: SLUSARZ
Copyright 2026 Tom Jeziorski. Trade Secret.
Kryptografia, tokeny, bezpieczenstwo, szyfrowanie
"""
import hashlib, hmac, base64, json, time, secrets

class Slusarz:
    NAME = "SLUSARZ"
    ICON = "🔐"
    VERSION = "2.0"
    
    def __init__(self, master_key=None):
        self.master_key = master_key or secrets.token_hex(32)
        self.vault = {}
        self.ops_count = 0
    
    def hash_sha256(self, data):
        self.ops_count += 1
        return {"algorithm": "SHA-256", "hash": hashlib.sha256(data.encode()).hexdigest()}
    
    def hmac_sign(self, data, key=None):
        k = (key or self.master_key).encode()
        self.ops_count += 1
        return {"signature": hmac.new(k, data.encode(), hashlib.sha256).hexdigest(), "algorithm": "HMAC-SHA256"}
    
    def hmac_verify(self, data, signature, key=None):
        k = (key or self.master_key).encode()
        expected = hmac.new(k, data.encode(), hashlib.sha256).hexdigest()
        self.ops_count += 1
        return {"valid": hmac.compare_digest(expected, signature)}
    
    def generate_token(self, payload, ttl_sec=3600):
        payload["iat"] = int(time.time())
        payload["exp"] = int(time.time()) + ttl_sec
        payload["jti"] = secrets.token_hex(8)
        data = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
        sig = hmac.new(self.master_key.encode(), data.encode(), hashlib.sha256).hexdigest()
        self.ops_count += 1
        return {"token": f"{data}.{sig}", "expires_in": ttl_sec, "jti": payload["jti"]}
    
    def verify_token(self, token):
        try:
            data, sig = token.rsplit(".", 1)
            expected = hmac.new(self.master_key.encode(), data.encode(), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(expected, sig):
                return {"valid": False, "error": "INVALID_SIGNATURE"}
            payload = json.loads(base64.urlsafe_b64decode(data))
            if payload.get("exp", 0) < time.time():
                return {"valid": False, "error": "EXPIRED"}
            return {"valid": True, "payload": payload}
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def vault_store(self, key, value):
        encrypted = base64.b64encode(value.encode()).decode()
        self.vault[key] = {"data": encrypted, "checksum": hashlib.sha256(value.encode()).hexdigest()[:16]}
        self.ops_count += 1
        return {"key": key, "stored": True}
    
    def vault_retrieve(self, key):
        if key not in self.vault:
            return {"error": f"Key {key} not found"}
        return {"key": key, "value": base64.b64decode(self.vault[key]["data"]).decode()}
    
    def generate_api_key(self, prefix="cu"):
        self.ops_count += 1
        return {"api_key": f"{prefix}_{secrets.token_urlsafe(32)}", "prefix": prefix}
    
    def generate_totp_secret(self):
        self.ops_count += 1
        return {"totp_secret": base64.b32encode(secrets.token_bytes(20)).decode(), "digits": 6, "period": 30}
    
    def password_hash(self, password, salt=None):
        salt = salt or secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000).hex()
        self.ops_count += 1
        return {"hash": hashed, "salt": salt, "algorithm": "PBKDF2-SHA256", "iterations": 100000}
    
    def report_to(self, coordinator):
        return {"module": self.NAME, "icon": self.ICON, "ops": self.ops_count,
                "vault_keys": len(self.vault), "status": "ACTIVE"}

if __name__ == "__main__":
    s = Slusarz()
    print(f"\n{s.ICON} === {s.NAME} v{s.VERSION} ===")
    print(f"Token: {s.generate_token({'user': 'TJ', 'role': 'owner'})}")
    print(f"API Key: {s.generate_api_key()}")
    print(f"TOTP: {s.generate_totp_secret()}")
