import subprocess

def is_device_available(adb_executable: str):
    """
    adb output could change depending on the platform 
    this is why there is a separate function to check
    if devices are available
    """
    command = [adb_executable, "devices"]
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF-8", check=False)
    try:
        workingoutput = result.stdout.lstrip().split('\n', 1)[1].strip()
        if workingoutput != '':
            return True
        return False
    except:
        return False
