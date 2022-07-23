"""Fun with exit and quit."""
import sys


def raiseexit() -> None:
    """Raise SystemExit"""
    raise SystemExit()


def use_method(method) -> None:
    """Use method."""
    for idx in range(2):
        print(idx)
        input("Press enter to test: ")
        try:
            method()
        except:
            print("Exception")


if __name__ == "__main__":
    selection = sys.argv[1] if len(sys.argv) > 1 else 1
    choices = {
        "1": (raiseexit, "raise SystemExit"),
        "2": (exit, "exit()"),
        "3": (quit, "quit()"),
        "4": (sys.exit, "sys.exit()"),
    }

    exc, label = choices.get(selection)
    if exc is None:
        print("Invalid selection")
    else:
        print("Running check with", label)
        use_method(exc)
    print("Done")
