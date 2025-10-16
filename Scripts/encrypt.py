import pyaes
import rsa
import hmac
import hashlib
import time
import lzma
import os

# CONF
RSAFILE = os.path.expanduser("~/scamsight.rsa.pubkey.pem")

def Encrypt(text: str) -> bytes:
    if isinstance(text, str):
        text = text.encode()
    with open(RSAFILE, "rb") as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read())

    AESkey = bytearray(os.urandom(32))
    iv = bytearray(os.urandom(16))

    timestamp = int(time.time()).to_bytes(8, "big")
    texttimestamp = timestamp + text

    pad = 16 - (len(text) % 16)
    paddedtext = bytearray(texttimestamp + bytes([pad] * pad))

    AES = pyaes.AESModeOfOperationCBC(bytes(AESkey), bytes(iv))
    encrypter = pyaes.Encrypter(AES)
    cipherdata = encrypter.feed(bytes(paddedtext)) + encrypter.feed()

    keyiv = AESkey + iv
    encryptedkeyiv = rsa.encrypt(keyiv, pubkey)

    hmackey = hashlib.sha256(AESkey).digest()
    h = hmac.new(hmackey, digestmod=hashlib.sha256)
    h.update(encryptedkeyiv)
    h.update(cipherdata)
    tag = h.digest()

    ret =  len(encryptedkeyiv).to_bytes(4, "big") + encryptedkeyiv + cipherdata + tag

    for i in range(len(AESkey)):
        AESkey[i] = 0
    for i in range(len(iv)):
        iv[i] = 0
    for i in range(len(paddedtext)):
        paddedtext[i] = 0   

    del AESkey, iv, paddedtext, tag
    
    ret = lzma.compress(ret)
    return ret