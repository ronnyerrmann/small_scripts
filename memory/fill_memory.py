import os
import random

data = []
while True:
    data1 = set()
    for i in range(1000):
        data1.add(f"{random.random}"*random.randint(1000,10000))
    data.append(data1)