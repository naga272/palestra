import time
import subprocess


tempi = []

for i in range(0, 1000, 1):
    start = time.time()
    subprocess.run("python main.py")
    tempi.append(time.time() - start)


print(sum(tempi) / len(tempi))
