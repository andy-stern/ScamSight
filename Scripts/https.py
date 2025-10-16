import ssl
import certifi
import requests
import asyncio
from requests.adapters import HTTPAdapter

class SecureHTTPAdapter(HTTPAdapter):
    def __init__(self):
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        self.ssl_context.set_ciphers("ECDHE+AESGCM:!aNULL:!eNULL:!MD5:!RC4")
        self.ssl_context.load_verify_locations(certifi.where())
        super().__init__()
    
    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

    def cert_verify(self, conn, url, verify, cert):
        return super().cert_verify(conn, url, verify, cert)
    
def Get(url, **kwargs):
    session = requests.Session()
    session.mount("https://", SecureHTTPAdapter())
    return session.get(url, timeout=25, **kwargs)

def Post(url, **kwargs):
    session = requests.Session()
    session.mount("https://", SecureHTTPAdapter())
    return session.post(url, timeout=25, **kwargs)

def AsyncPost(url, **kwargs):
    return asyncio.to_thread(Post, url, **kwargs)
