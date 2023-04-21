import sys
from src.core import *      # pylint: disable=W0401, W0614
from src.termux_utils import *  # pylint: disable=W0401, W0614

_platform = platform.system()
ADB_COMMAND = "adb.exe" if _platform == "Windows" else "adb"

def print_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(1.5)
    print("  __    ___  ____ ")
    print(" / _\\  / __)/ ___)")
    print("/    \\| (_  \\ ___\\")
    print("\\_/\\_/ \\___/(____/")
    for item in menu_options.items():
        print(item[0], '--', item[1])


menu_options = {
    1: 'Setup system [MUST if first time]',
    2: 'Create new repo',
    3: 'List all active repositories',
    4: 'Get clone command',
    5: 'Try to find the IP of your device',
    6: "Delete repo",
    7: 'Exit',
}

if __name__ == '__main__':
    check_everything()
    while True:
        print_menu()
        option = int(input('Enter your choice: '))
        if option == 1:
            setup_system(ADB_COMMAND)
        elif option == 2:
            create_new_repository()
        elif option == 3:
            list_all_active_repos()
        elif option == 4:
            get_clone_command()
        elif option == 5:
            find_device_arp_info()
        elif option == 6:
            delete_repo()
        elif option == 7:
            sys.exit()
        else:
            print('Invalid option. Please enter a number between 1 and 3.')
