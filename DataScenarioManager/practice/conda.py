import subprocess

# Conda 환경 이름
env_name = 'base'

# 실행할 Python 스크립트 또는 명령
script_to_run = 'main.py'

# Conda 환경을 활성화하고 Python 스크립트를 실행하는 명령
command = f"conda run -n {env_name} python {script_to_run}"

# subprocess로 명령 실행
try:
    # 명령을 쉘에서 실행
    result = subprocess.run(command, shell=True, check=True, text=True)
    print("Execution succeeded:", result.stdout)
except subprocess.CalledProcessError as e:
    print("An error occurred while executing the script:", e)
