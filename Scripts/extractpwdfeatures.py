from collections import Counter
from .asciientropy import Score
from .shannonentropy import ShannonEntropy

def Extract(password: str) -> dict:
    features = {}

    if not password:
        return features

    features["length"] = len(password)
    features["nuppers"] = sum(1 for c in password if c.isupper())
    features["nlowers"] = sum(1 for c in password if c.islower())
    features["ndigits"] = sum(1 for c in password if c.isdigit())
    features["nsymbols"] = sum(1 for c in password if not c.isalnum())

    counter = Counter(password)
    features["chuniques"] = len(counter)
    features["chdiversity"] = len(counter) / len(password)

    features["asciientropy"] = Score(password) * 14
    features["shannonentropy"] = ShannonEntropy(password)

    features["nseqletters"] = sum(1 for i in range(len(password) - 2) if ord(password[i+1]) == ord(password[i]) + 1 and password[i].isalpha())
    features["nseqdigits"] = sum(1 for i in range(len(password) - 2) if ord(password[i+1]) == ord(password[i]) + 1 and password[i].isdigit())

    features["nrepeats"] = sum(password.count(c * 2) for c in set(password))
    
    return features