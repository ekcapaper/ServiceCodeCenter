import json
import time

a = 1
while True:
    with open("a.txt", "w", encoding="utf-8") as f:
        f.write(str(a))
    time.sleep(1)

