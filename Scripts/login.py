import json
import os
import stat
from .https import Post

# CONF
AUTHFILE = os.path.expanduser("~/scamsight.auth.json")
RSAFILE = os.path.expanduser("~/scamsight.rsa.pubkey.pem")


def saveauth(data):
    with open(AUTHFILE, "w") as f:
        json.dump(data, f)
        
    os.chmod(AUTHFILE, stat.S_IRUSR | stat.S_IWUSR)

def Login(email: str, password: str) -> int:
    try:
        response = Post(
            "https://api.scamsight.app/login",
            json={"email": email, "password": password},
        )
        result = response.json()
        if result.get("ok"):
            if response.status_code == 200:
                token = result.get("token")
                userid = result.get("userid")
                upub = Post(
                    "https://api.scamsight.app/getpublickey",
                    headers={
                        "Authorization": token
                    }
                ).json().get("publickey")
                if upub:
                    with open(RSAFILE, "w") as f:
                        f.write(upub)
                saveauth({"token": token, "userid": userid})
                return 200
            elif response.status_code == 201:
                return 201
        
        if response.status_code == 400:
            return 400
        elif response.status_code == 401:
            return 401
        elif response.status_code == 403:
            return 403
        elif response.status_code == 500:
            return 500
        elif response.status_code == 429:
            return 429
    except Exception:
        return 500
