import subprocess

def run_in_conda_env(env_name, command):
    full_command = f"conda run -n {env_name} {command}"
    result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr