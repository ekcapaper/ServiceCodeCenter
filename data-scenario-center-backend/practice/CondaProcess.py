import time
import subprocess

process = subprocess.Popen(["ping", "google.com"])

time.sleep(2)

process.terminate()
process.wait()
print("subprocess has been terminated")