import os
import re
from src.logg import logg, print_exception
from src.termux_utils import run_command_in_termux

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


def export_pub_key_in_termux_sshd():
    print("Coping public key into the ssh server")
    with open(f"{HOME}/.ssh/ags-key.pub", encoding="utf-8") as f:
        pub_key = f.read()
        run_command_in_termux("cd /data/data/com.termux/files/home/")
        pub_key = pub_key.replace('\n', '').replace('\r', '')
        run_command_in_termux(
            f'echo {pub_key} \\>\\> .ssh/authorized_keys')
