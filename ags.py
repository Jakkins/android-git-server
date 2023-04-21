import sys
from src.core import check_everything, create_new_repository, delete_repo, find_device_arp_info, get_clone_command, list_all_active_repos, open_termux, setup_system

menu_options = {
    1: 'Setup system',
    2: 'Create new repo',
    3: 'List all active repositories',
    4: 'Get clone command',
    5: 'Try to find the IP of your device',
    6: "Delete repo",
    7: 'Exit',
}

def print_menu():
    for item in menu_options.items():
        print(item[0], '--', item[1])

if __name__ == '__main__':
    check_everything()
    open_termux(2)
    # start_ssh() ssh should start alone using Termux:Boot app
    while True:
        print_menu()
        option = int(input('Enter your choice: '))
        if option == 1:
            setup_system()
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
