import subprocess as s
from time import sleep


s.run('ls', shell=True)

for i in range(0, 10):
    sleep(1)
    print("\nyes")
