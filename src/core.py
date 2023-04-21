import codecs
import os
import os.path
import socket
import subprocess
import platform
import time
import re
import sys
from src.common.utils import is_installed
from src.logg import print_exception
from src.adb_utils import adb_windows

AGS_PATH = "/data/data/com.termux/files/home/android-git-server-utils"
HOME = os.path.expanduser("~")


def get_escaped_string(str_to_decode: str) -> str:
    return codecs.decode(str_to_decode, 'unicode_escape')


def open_termux(sleep):
    os.system("adb shell am start -n com.termux/.HomeActivity")
    time.sleep(sleep)


def run_command_in_termux(command):
    """
    lot of chars are NOT escaped be aware
    """
    if '\n' in command:
        print("Illegal character new line in command")
        return
    command = command.replace(" ", "%s")
    os.system(f'adb shell input text "{command}"')
    os.system('adb shell input keyevent ENTER')


def start_ssh():
    try:
        run_command_in_termux("sshd")
        os.system('adb forward tcp:8022 tcp:8022')
        print("If the system is already setted up, you can ssh with:")
        print(f"     ssh -i {HOME}\\.ssh\\ags-key -p 8022 localhost")
        # os.system(f"git config core.sshCommand \"ssh -i {home}/.ssh/ags-key -o IdentitiesOnly=yes\"")
    except:
        pass


def create_new_repository():
    repo_name = input('Insert name of the repository: ')
    if not repo_name.endswith('.git'):
        repo_name = repo_name + ".git"
    run_command_in_termux(f"mkdir -p {AGS_PATH}/repos/{repo_name}")
    run_command_in_termux(
        f"git init --bare {AGS_PATH}/repos/{repo_name}")
    print(f"Initialized git repo in {AGS_PATH}/repos/{repo_name}")
    print("You can use:")
    print("     git clone ssh://git@mydomain:[port]/projectname.git")
    print(
        f"     git clone ssh://localhost:8022/data/data/com.termux/files/home/android-git-server-utils/repos/{repo_name}")


def create_ssh_key_pair():
    if not os.path.exists(f"{HOME}/.ssh"):
        print("Please install OpenSSH")
        return
    if (os.path.exists(f"{HOME}/.ssh/ags-key") and os.path.exists(f"{HOME}/.ssh/ags-key.pub")):
        print("Key pair already exists")
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
    print("Coping public key into the ssh server")
    with open(f"{HOME}/.ssh/ags-key.pub", encoding="utf-8") as f:
        pub_key = f.read()
        run_command_in_termux("cd /data/data/com.termux/files/home/")
        pub_key = pub_key.replace('\n', '').replace('\r', '')
        run_command_in_termux(
            f'echo {pub_key} \\>\\> .ssh/authorized_keys')
    print("Checking ssh configuration")
    with open(f"{HOME}/.ssh/config", "a+", encoding="utf-8") as f:
        f.seek(0)
        config = f.read()
        line = re.findall('\\s(ags)\\s', config)
        if not line:
            f.writelines(
                ["\n\nHost localhost", "\n  HostName localhost", "\n  User ags", f"\n  IdentityFile {HOME}/.ssh/ags-key"])


def setup_system():
    open_termux(2)
    print("Updating")
    run_command_in_termux("apt update \\&\\& apt -y upgrade")
    print("Installing git and openssh")
    run_command_in_termux("apt install git openssh")
    run_command_in_termux("sshd")
    create_ssh_key_pair()


def find_device_arp_info():
    with os.popen('arp -a') as f:
        data = f.read()
    for line in re.findall('([-.0-9]+)\\s+([-0-9a-f]{17})\\s+(\\w+)', data):
        try:
            print(socket.gethostbyaddr(line[0]))
        except:
            pass


def get_all_active_repo():
    cmd_literal = f"ssh -i {HOME}\\.ssh\\ags-key -p 8022 localhost ls ./android-git-server-utils/repos"
    result = subprocess.run(cmd_literal.split(
        " "), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF-8", check=False)
    if result.returncode != 0:
        print("STDERR:", result.stderr)
        return ""
    return result.stdout


def list_all_active_repos():
    repos = get_all_active_repo()
    if repos:
        print(repos)


def print_repo_menu() -> (dict[int, str] | None):
    repos = get_all_active_repo()
    if repos:
        if repos.endswith("\n"):
            repos = repos[:-1]
        list_of_repos = repos.split("\n")
        repos_dict = {}
        for idx, repo in enumerate(list_of_repos):
            repos_dict[idx] = repo
        for item in repos_dict.items():
            print(item[0], '--', item[1])
        return repos_dict


def get_clone_command():
    repos_dict = print_repo_menu()
    if repos_dict:
        try:
            _choice = int(input('Choose a repository: '))
            if _choice <= len(repos_dict):
                print(
                    f"git clone ssh://localhost:8022/data/data/com.termux/files/home/android-git-server-utils/repos/{repos_dict[_choice]}")
        except:
            pass


def delete_repo():
    repos_dict = print_repo_menu()
    if repos_dict:
        try:
            _choice = int(input('Choose a repository: '))
            if _choice <= len(repos_dict):
                _yn = input(
                    f'You sure you want to delete {repos_dict[_choice]}? [type name of repo] ')
                if _yn == repos_dict[_choice]:
                    open_termux(1)
                    run_command_in_termux(f"rm -r {AGS_PATH}/repos/{_yn}")
        except:
            pass


def check_everything():
    # python version
    if sys.version_info[0] < 3:
        print_exception("Python 3 or a more recent version is required.")
    # adb installed?
    # or is ssh installed?
    _platform = platform.system()
    if _platform == "Windows":
        if not is_installed("adb.exe"):
            print_exception("Install adb first.")
        if not is_installed("ssh.exe"):
            print_exception("Install ssh first.")
    elif _platform == "Linux" or _platform == "Darwin":
        if not is_installed("adb"):
            print_exception("Install adb first.")
        if not is_installed("ssh"):
            print_exception("Install ssh first.")
    # device connected?
    if _platform == "Windows":
        if not adb_windows.is_device_available("adb.exe"):
            print_exception("None device connected")

	# check ags-keys