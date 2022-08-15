import random
import time

import psutil


data = []
while True:
    data1 = set()
    for i in range(1000):
        data1.add(f"{random.random}"*random.randint(1000,10000))
    data.append(data1)
    if psutil.virtual_memory().percent > 80:
        time.sleep(2)