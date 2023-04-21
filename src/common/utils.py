import subprocess


def is_installed(program):
    result = subprocess.run(program, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF-8", check=False)
    return result is not None
