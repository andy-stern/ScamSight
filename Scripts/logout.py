import os
import json
from .https import Post

# CONF
AUTHFILE = os.path.expanduser("~/scamsight.auth.json")

def Logout() -> int:
    try:
        token = ""
            
        try: 
            with open(AUTHFILE) as f:
                authdata = json.load(f)

            token = authdata.get("token")
        except Exception:
            pass
            
        if not token:
            return
            
        response = Post(
            "https://api.scamsight.app/logout",
            headers={"Authorization": token}
        )
        result = response.json()
        if result.get("ok"):
            os.remove(AUTHFILE)
            return 200

        if response.status_code == 403:
            return 403
        elif response.status_code == 500:
            return 500
    except Exception:
        return 500