import subprocess


def is_installed(program):
    command = program.split(' ')
    result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL, encoding="UTF-8", check=False)
    return result is not None


def read_file_content(file_path, encoding: str):
    if encoding is None:
        encoding = "UTF-8"
    with open(file_path, "r", encoding=encoding) as file:
        content = file.read()
    return content
