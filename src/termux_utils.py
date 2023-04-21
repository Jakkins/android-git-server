import os
import platform
import time
from src.logg import logg
from src.windows_utils.ssh import export_pub_key_in_termux_sshd

_platform = platform.system()
ADB_COMMAND = "adb.exe" if _platform == "Windows" else "adb"


def run_command_in_termux(command):
    """
    Lots of chars are NOT escaped be aware.
    To work this method need the device to has termux
    opened in the foreground.
    """
    if '\n' in command:
        print("Illegal character new line in command")
        return
    command = command.replace(" ", "%s")
    os.system(f'adb shell input text "{command}"')
    os.system('adb shell input keyevent ENTER')


def open_termux(adb_command, sleep):
    os.system(f"{adb_command} shell am start -n com.termux/.HomeActivity")
    time.sleep(sleep)


def wait_for_user_to_switch_on_screen():
    logg().warning("##################")
    print("Switch on the smartphone screen before proceed!")
    print("Click any key to continue")
    logg().warning("##################")
    input('')


def setup_system(adb_command):
    wait_for_user_to_switch_on_screen()
    open_termux(adb_command, 2)
    logg().warning("updating termux, check the smartphone!")
    run_command_in_termux("apt update \\&\\& apt -y upgrade")
    run_command_in_termux("apt install git openssh bash")
    input('click to continue ')
    if _platform == "Windows":
        export_pub_key_in_termux_sshd()
    