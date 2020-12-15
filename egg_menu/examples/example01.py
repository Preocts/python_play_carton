#! usr/bin/python3.8
""" Sample use of library

Author: Preocts, preocts@preocts.com
Git   : https://github.com/Preocts/egg_menu
"""
from eggmenu import egg_menu


def example01() -> str:
    print("This is a simple function with no arguments")
    return "Ran example01 successfully!"


def example02(value01: int, value02: int) -> str:
    print('This function has two positional arguments.', end='')
    print(f' value01 = {value01}, value02 = {value02}')
    return "Ran example02 successfully!"


def example03(**kwargs) -> str:
    print('This function takes only keyword arguments.')
    print(f'Keywords: {kwargs}')
    return "Ran example03 successfully!"


def example04(*args, **kwargs) -> str:
    print('This function takes position and keyword arguments')
    print(f'Positional: {args}')
    print(f'Keywords: {kwargs}')
    return "Ran example04 successfully!"


def menu_exit():
    exit()


def main():
    # Create the menu object
    menu = egg_menu.Egg_Menu()

    # Update menu title
    menu.set_title("This is an example menu:")

    # Add our menu choices
    menu.add_choice('Example Option 1', example01)
    menu.add_choice('Example Option 2', example02, 15, 30)
    menu.add_choice('Example Option 3', example03, my_kwargs='Example')
    menu.add_choice('Example Option 4', example04, "Hello", world="Goodbye")
    menu.add_choice('Exit', menu_exit)

    # Enter menu loop
    while True:
        # Clear the screen
        menu.clear_screen()

        # Print the menu
        menu.print_menu()

        # Get user input
        my_choice = input('Enter your choice: ')

        # Execute command
        return_value = menu.run_command(my_choice)
        print(f'\n{return_value}')

        # Pause for key input before continuing
        input('Press enter to continue...')


if __name__ == '__main__':
    main()
