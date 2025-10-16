import math
from collections import Counter

def ShannonEntropy(s: str) -> float:
    if not s:
        return 0.0
    
    counter = Counter(s)
    length = len(s)
    return -sum((count / length) * math.log2(count / length) for count in counter.values())