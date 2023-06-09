import platform
from src.logg import logg
from src.termux.termux_utils import open_termux, run_command_in_termux, wait_for_user_to_switch_on_screen
from src.common.ssh import export_pub_key_in_termux_sshd

_platform = platform.system()
ADB_COMMAND = "adb.exe" if _platform == "Windows" else "adb"

def setup_system(adb_command):
    wait_for_user_to_switch_on_screen()
    open_termux(adb_command, 2)
    logg().warning("updating termux, check the smartphone!")
    run_command_in_termux("apt update \\&\\& apt -y upgrade")
    run_command_in_termux("apt install git openssh bash")
    export_pub_key_in_termux_sshd()
