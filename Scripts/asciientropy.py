import os
import math
import struct
from collections import Counter

# CONF
CHUNKSIZE = struct.calcsize("cf")

asciidata = {}

def Score(s: str) -> float:
    if not s:
        return 0.0
    
    if not asciidata:
            with open(os.path.join(os.path.dirname(__file__), "asciidata.bin"), "rb") as f:
                while True:
                    chunk = f.read(CHUNKSIZE)
                    if len(chunk) != CHUNKSIZE:
                        break
                    ch, freq = struct.unpack("cf", chunk)
                    c = ch.decode("ascii")
                    if c.isalpha():
                        c = c.lower()
                    asciidata[c] = freq
    
    s = s.lower()
    counter = Counter(s)
    slen = len(s)
    
    entropy = 0.0
    for c, count in counter.items():
        if c == ' ':
            freq = 0.02
        else:
            freq = asciidata.get(c, 1e-6)
        
        entropy += count * -math.log2(freq)
    
    normalized = entropy / slen / 14.0
    diversity = len(counter) / slen
    lenfactor = math.log2(slen + 1) / 6.0
    
    return min(normalized * (0.5 + 0.5 * diversity) * lenfactor, 1.0)