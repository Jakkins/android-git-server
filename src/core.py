import codecs
import os
import os.path
import socket
import platform
import re
import sys
from src.termux.termux_utils import run_command_in_termux
from src.common.utils import is_installed
from src.logg import logg, print_exception
from src.common import adb
from src.common import ssh

_platform = platform.system()
ADB_COMMAND = "adb.exe" if _platform == "Windows" else "adb"
SSH_V_COMMAND = "ssh.exe -v" if _platform == "Windows" else "ssh -v"
SSH_COMMAND = "ssh.exe" if _platform == "Windows" else "ssh"
AGS_PATH = "/data/data/com.termux/files/home/android-git-server-utils"
HOME = os.path.expanduser("~")


def get_escaped_string(str_to_decode: str) -> str:
    return codecs.decode(str_to_decode, 'unicode_escape')


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
    input('click any key to continue')


def find_device_arp_info():
    with os.popen('arp -a') as f:
        data = f.read()
    for line in re.findall('([-.0-9]+)\\s+([-0-9a-f]{17})\\s+(\\w+)', data):
        try:
            print(socket.gethostbyaddr(line[0]))
        except:
            pass
    input('click any key to continue')


def get_all_active_repo():
    command_string = "ls ./android-git-server-utils/repos"
    result = ssh.run_command_with_ssh(command_string)
    if result == "":
        return "None active repo found"
    return result


def list_all_active_repos():
    repos = get_all_active_repo()
    if repos:
        print(repos)
    input('click any key to continue')


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
            _choice = int(input('choose a repository: '))
            if _choice <= len(repos_dict):
                print(
                    f"git clone ssh://localhost:8022/data/data/com.termux/files/home/android-git-server-utils/repos/{repos_dict[_choice]}")
                input('click any key to continue')
        except:
            pass


def delete_repo():
    repos_dict = print_repo_menu()
    if repos_dict:
        try:
            _choice = int(input('choose a repository: '))
            if _choice <= len(repos_dict):
                _yn = input(
                    f'You sure you want to delete {repos_dict[_choice]}? [type name of repo] ')
                if _yn == repos_dict[_choice]:
                    # right/path/is/like/this
                    command_string = f"rm -r {AGS_PATH}/repos/{_yn}"
                    ssh.run_command_with_ssh(command_string)
        except:
            pass
    input('click any key to continue')


def check_everything():
    logg().info("check python version")
    if sys.version_info[0] < 3:
        print_exception("Python 3 or a more recent version is required.")
    logg().info("check adb, ssh installed")
    if not is_installed(ADB_COMMAND):
        print_exception("Install adb first.")
    if not is_installed(SSH_V_COMMAND):
        print_exception("Install ssh first.")
    logg().info("check if device is connected")
    if not adb.is_device_available(ADB_COMMAND):
        print_exception("None device connected")
    logg().info("check ags-keys")
    if not ssh.are_keys_present():
        ssh.create_ssh_key_pair()
    else:
        logg().info("ags-keys already present")
    ssh.create_ssh_configuration()  # auto check for configuration presence
    os.system('adb forward tcp:8022 tcp:8022')


def get_dir_path():
    while True:
        dir_path = input("Enter a directory path: ")
        if os.path.isdir(dir_path):
            return dir_path
        logg().warning("Directory does not exist. Please try again.")


def clone_a_repo():
    dir_path = get_dir_path()
    repos_dict = print_repo_menu()
    if repos_dict:
        _username = ""
        _email = ""
        try:
            _choice = int(input('choose a repository: '))
            if _choice <= len(repos_dict):
                clone_command = f"git clone ssh://localhost:8022/data/data/com.termux/files/home/android-git-server-utils/repos/{repos_dict[_choice]}"
                _username = input(
                    'insert username (default: none): ') or "none"
                _email = input('insert email (default: none): ') or "none"
                os.chdir(dir_path)
                os.system(clone_command)
                repo_name = repos_dict[_choice]
                if not repo_name.endswith('.git'):
                    repo_name = repo_name.replace(".git", "")
                os.chdir(os.path.join(dir_path, repo_name))
                os.system('git config user.name "' + _username + '"')
                os.system('git config user.email "' + _email + '"')
                input('click any key to continue')
        except:
            logg().error("exception occurred")
            logg().info("remember to:")
            print('git config user.name %s', _username)
            print('git config user.email %s', _email)
            input('click any key to continue')
