import os
import time
from src.logg import logg


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
    