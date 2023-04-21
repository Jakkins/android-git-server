import subprocess


def is_installed(program):
    command = program.split(' ')
    result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL, encoding="UTF-8", check=False)
    return result is not None
