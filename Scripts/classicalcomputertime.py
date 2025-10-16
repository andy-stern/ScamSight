import math
import string

CLASSICALRATE = 1000000000
SUPERSCRIPTS = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")
PREFIXES = {
    -30: "quecto",
    -27: "ronto",
    -24: "yocto",
    -21: "zepto",
    -18: "atto",
    -15: "femto",
    -12: "pico",
    -9:  "nano",
    -6:  "micro",
    -3:  "milli",
    0:  "",
    3:  "kilo",
    6:  "mega",
    9:  "giga",
    12:  "tera",
    15:  "peta",
    18:  "exa",
    21:  "zetta",
    24:  "yotta",
    27:  "ronna",
    30:  "quetta"
}

def _charsetsize(password: str):
    haslower = any(c.islower() for c in password)
    hasupper = any(c.isupper() for c in password)
    hasdigit = any(c.isdigit() for c in password)
    hassymbol = any((not c.isalnum()) for c in password)
    
    size = 0
    if haslower: 
        size += 26
    if hasupper: 
        size += 26
    if hasdigit: 
        size += 10
    if hassymbol: 
        size += len(string.punctuation)
    if size == 0: 
        size = len(set(password)) or 1
    return size

def ClassicalPasswordTime(password: str, rate: float):
    length = len(password)
    if length == 0: 
        return "Zero seconds to crack this password."
    
    charsetsize = _charsetsize(password)
    N = charsetsize ** length
    
    seconds = N / (2.0 * rate)
    
    exp = int(math.floor(math.log10(seconds) / 3)) * 3 if seconds > 0 else 0
    exp = max(min(exp, 30), -30)
    
    factor = 10.0 ** exp
    prefix = PREFIXES.get(exp, f"e{exp}")
    
    mant = seconds / factor
    if mant >= 100: 
        fmt = "{:.0f}"
    elif mant >= 10: 
        fmt = "{:.1f}"
    else: 
        fmt = "{:.2f}"
        
    log10seconds = math.log10(seconds) if seconds > 0 else 0
    
    sciexp = int(math.floor(log10seconds))
    scimant = 10 ** (log10seconds - sciexp)
    if scimant >= 100: 
        sfmt = "{:.0f}"
    elif scimant >= 10: 
        sfmt = "{:.1f}"
    else:
        sfmt = "{:.2f}"
    
    pname = (prefix + "seconds") if prefix else "seconds"
    return f"{fmt.format(mant)} {pname} ({sfmt.format(scimant)} × 10{str(sciexp).translate(SUPERSCRIPTS)} seconds) to crack this password."