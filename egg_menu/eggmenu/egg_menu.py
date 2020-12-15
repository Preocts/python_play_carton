#! usr/bin/python3
""" Simple text menu for running commands

Author: Preocts, preocts@preocts.com
Git   : https://github.com/Preocts/egg_menu
"""
import os
from typing import Any


class Egg_Menu(object):
    """ Simple menus """

    def __init__(self):
        self.__menu_title = "Menu Selections:"
        self.__menu_items = {}
        return

    def __str__(self):
        return str(self.__menu_items)

    def __bool__(self):
        return True if self.__menu_items else False

    def __iter__(self):
        return iter(self.__menu_items.values())

    def __next__(self) -> dict:
        if not hasattr(self, '_iter'):
            self._iter = iter(self.__menu_items.values())
        return next(self._iter)

    def set_title(self, title: str) -> bool:
        """ Sets the title of the menu """
        if not isinstance(title, str):
            return False
        self.__menu_title = title

    def add_choice(self, label: str, func: object, *args, **kwargs) -> bool:
        """ Add a menu option. "Label", function, (args), (kwargs)

            Any arguments or keyword arguments to be run with the function
            should be passed here.
        """
        try:
            self.__menu_items[label] = {
                'name': label,
                'function': func,
                'args': args,
                'kwargs': kwargs
            }
        except Exception:
            return False
        return True

    def del_choice(self, label: str) -> bool:
        """ Delete a menu option, "Label" """
        if label not in self.__menu_items:
            return False
        del self.__menu_items[label]
        return True

    def clear_screen(self) -> None:
        """ Clears screen, should work on most systems """
        os.system('cls||clear')  # Clear screen on NT or *nix systems

    def print_menu(self) -> None:
        """ Prints menu """
        print(self.__menu_title)
        for count, label in enumerate(self.__menu_items.keys()):
            print(f'\t{count + 1}) {label}')
        return

    def run_command(self, menu_choice: str) -> Any:
        """ Runs stored command by menu # """
        return_value = None
        try:
            count = int(menu_choice)
        except ValueError:
            print("Invalid input, menu options must be integers.")
            return return_value
        options = list(self.__menu_items)
        try:
            opt = options[count - 1]
        except IndexError:
            print("Invalid option.")
            return return_value

        if self.__menu_items[opt]['args'] and self.__menu_items[opt]['kwargs']:
            return_value = self.__menu_items[opt]['function'](
                *self.__menu_items[opt]['args'],
                **self.__menu_items[opt]['kwargs']
            )
        elif self.__menu_items[opt]['args']:
            return_value = self.__menu_items[opt]['function'](
                *self.__menu_items[opt]['args']
            )
        elif self.__menu_items[opt]['kwargs']:
            return_value = self.__menu_items[opt]['function'](
                **self.__menu_items[opt]['kwargs']
            )
        else:
            return_value = self.__menu_items[opt]['function']()

        return return_value
