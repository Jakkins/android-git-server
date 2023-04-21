
import os


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
