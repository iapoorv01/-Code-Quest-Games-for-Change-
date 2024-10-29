import numpy as np
import random
prices=np.array([1399,6298,10999,14999,7298,6385,8999,9999,9999,13868])
model=np.array(["Samsung Galaxy M30G","Realme C2","Xiaomi Redmi Note 7 Pro","Xiaomi Redmi Note 8 Pro","Realme C2 32GB","Realme C2 2GB RAM","Realme 5","Xiaomi Redmi Note 75 64Gb","Xiaomi Redmi Note 8","Vivo Z1 PRO"])

price=np.array([1399,6298,10999,14999,7298,6385,8999,9999,9999,13868])
p=prices*price
print(f"Total Cost:{np.sum(p)}")
print(f"min:{np.min(prices)}")
print(f"max:{np.max(prices)}")
print(f"mean:{np.mean(p)}")
from collections import Counter
def mode(prices):
    price_count = Counter(prices)
   # print(price_count)
    print(max(price_count.values()))
    max_count = max(price_count.values())
    modes = [price for price, count in price_count.items() if count == max_count]
    return modes[0] if len(modes) == 1 else modes


print("Mode:", mode(prices))