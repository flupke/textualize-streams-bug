import time
import sys

i = 0
while True:
    print(i)
    i += 1
    time.sleep(0.1)
    sys.stdout.flush()
