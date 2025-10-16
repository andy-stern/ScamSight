import os
import rsa
from .https import Post

# CONF
RSAFILE = os.path.expanduser("~/scamsight.rsa.pubkey.pem")

def Register(email: str, password: str) -> int:
    try:
        response = Post("https://api.scamsight.app/register", json={"email": email, "password": password})
        result = response.json()
        if result.get("ok"):
            key = bytes(result.get("upub"), "utf-8")
            pubkey = rsa.PublicKey.load_pkcs1(key)
            with open(RSAFILE, "wb") as f:
                f.write(pubkey.save_pkcs1())
            return 200
        
        if response.status_code == 400:
            return 400
        elif response.status_code == 401:
            return 401
        elif response.status_code == 500:
            return 500
        elif response.status_code == 429:
            return 429
    except Exception as e:
        return 500