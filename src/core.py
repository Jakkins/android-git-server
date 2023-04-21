import codecs
import os
import os.path
import socket
import subprocess
import platform
import time
import re
import sys
from src.termux_utils import run_command_in_termux
from src.common.utils import is_installed
from src.logg import logg, print_exception
import src.windows_utils.adb as w_adb
import src.windows_utils.ssh as w_ssh


AGS_PATH = "/data/data/com.termux/files/home/android-git-server-utils"
HOME = os.path.expanduser("~")


def get_escaped_string(str_to_decode: str) -> str:
    return codecs.decode(str_to_decode, 'unicode_escape')


def open_termux(sleep):
    os.system("adb shell am start -n com.termux/.HomeActivity")
    time.sleep(sleep)


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


def setup_system():
    open_termux(2)
    print("Updating")
    run_command_in_termux("apt update \\&\\& apt -y upgrade")
    print("Installing git and openssh")
    run_command_in_termux("apt install git openssh")


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
    logg().info("check python version")
    if sys.version_info[0] < 3:
        print_exception("Python 3 or a more recent version is required.")
    logg().info("check adb, ssh, ssh-keygen installed")
    _platform = platform.system()
    if _platform == "Windows":
        if not is_installed("adb.exe"):
            print_exception("Install adb first.")
        if not is_installed("ssh.exe -v"):
            print_exception("Install ssh first.")
    elif _platform == "Linux" or _platform == "Darwin":
        if not is_installed("adb"):
            print_exception("Install adb first.")
        if not is_installed("ssh -v"):
            print_exception("Install ssh first.")
    logg().info("check if device is connected")
    if _platform == "Windows":
        if not w_adb.is_device_available("adb.exe"):
            print_exception("None device connected")
    logg().info("check ags-keys")
    if not w_ssh.are_keys_present("ags-key"):
        w_ssh.create_ssh_key_pair()
    else:
        logg().info("ags-keys already present")
    w_ssh.create_ssh_configuration()  # auto check for configuration presence
    # logg().warning("You should setup the system (Option 1).")
