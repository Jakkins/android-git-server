import os
import re
from src.common.utils import read_file_content
from src.logg import logg, print_exception
from src.termux.termux_utils import run_command_in_termux

HOME = os.path.expanduser("~")


def are_keys_present(key_name):
    privk = os.path.join(HOME, ".ssh", key_name)
    pubk = os.path.join(HOME, ".ssh", key_name+".pub")
    logg().info(f"checking keys presence in {HOME}")
    if not os.path.exists(privk):
        logg().warning("private key not found.")
    if not os.path.exists(pubk):
        logg().warning("public key not found.")
    return os.path.exists(privk) and os.path.exists(pubk)


def create_ssh_key_pair():
    if not os.path.exists(f"{HOME}/.ssh"):
        print_exception(f".ssh dir in {HOME} is missing. ssh missing?")
    if (os.path.exists(f"{HOME}/.ssh/ags-key") and os.path.exists(f"{HOME}/.ssh/ags-key.pub")):
        logg().info("key pair already exists")
        # should i re-add the public key? (no, you are going to check manually.)
        return
    try:
        os.remove(f"{HOME}/.ssh/ags-key")
    except:
        pass
    try:
        os.remove(f"{HOME}/.ssh/ags-key.pub")
    except:
        pass
    print("Creating key pair")
    os.system(
        f'cd {HOME}/.ssh && ssh-keygen -o -t ed25519 -C "ags" -f "ags-key" -N "''"')


def create_ssh_configuration():
    """
    Will check if the configuration is already present.
    Will work only in localhost mode.
    """
    logg().info("checking ssh configuration")
    with open(f"{HOME}/.ssh/config", "a+", encoding="utf-8") as f:
        f.seek(0)
        config = f.read()
        line = re.findall('\\s(ags)\\s', config)
        if not line:
            f.writelines(
                ["\n\nHost localhost", "\n  HostName localhost", "\n  User ags", f"\n  IdentityFile {HOME}/.ssh/ags-key"])

def get_pub_key():
    return read_file_content(f"{HOME}/.ssh/ags-key.pub", "UTF-8")


def export_pub_key_in_termux_sshd():
    # check if pubk already present in authorized_keys
    pubk = get_pub_key()
    pubk = pubk.replace('\n', '').replace('\r', '')
    run_command_in_termux("mkdir -p /data/data/com.termux/files/home/.ssh/")
    run_command_in_termux("bash")
    pubk_key_str = pubk.split(" ")[1]
    run_command_in_termux(f'result=\\$\\(grep -e {pubk_key_str} /data/data/com.termux/files/home/.ssh/authorized_keys\\)\\;')
    command = f"""
    if \\[ -z '$result' \\]\\; then echo {pubk} \\>\\> /data/data/com.termux/files/home/.ssh/authorized_keys\\; else echo key already added\\; fi
	""".strip().replace("\n", "")
    run_command_in_termux(command)
    run_command_in_termux("cat /data/data/com.termux/files/home/.ssh/authorized_keys")
