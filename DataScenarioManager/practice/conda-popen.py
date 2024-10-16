import subprocess
import signal
import sys
import threading
import time

# Conda 환경 이름
env_name = 'base'

# 실행할 Python 스크립트 또는 명령
script_to_run = 'main.py'

# Conda 환경을 활성화하고 Python 스크립트를 실행하는 명령
command = f"conda run -n {env_name} python {script_to_run}"
process = None

# 프로세스를 실행하는 함수
def run_command(command):
    global process
    try:
        # subprocess로 명령 실행
        process = subprocess.Popen(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 프로세스의 출력을 실시간으로 표시
        for line in process.stdout:
            print(line, end='')

        # 프로세스 종료 대기
        process.wait()
        print("Execution finished with return code:", process.returncode)

    except subprocess.CalledProcessError as e:
        print("An error occurred while executing the script:", e)

def stop_process():
    global process
    time.sleep(5)
    process.terminate()

thread = threading.Thread(target=stop_process())
thread.start()
# 명령 실행
run_command(command)
