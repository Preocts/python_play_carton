import os
import time
import random
import colorama


def clearScreen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def assembleBoard(xsize: int, ysize: int) -> tuple:
    """ Create the play board """
    xsize = xsize if xsize <= 80 else 80
    ysize = ysize if ysize <= 24 else 24
    board = []
    row_segment = []

    for idx in range(0, xsize):
        row_segment.append(0)

    for idx in range(0, ysize):
        board.append(row_segment)
    return board_to_tuple(board)


def seedBoard(gameBoard: tuple, chance: int):
    """ Seeds the game board with life """
    newBoard = board_to_list(gameBoard)
    for row_idx, row in enumerate(gameBoard):
        for square_idx, square in enumerate(row):
            dice_roll = random.randint(0, 100)
            if dice_roll <= chance:
                newBoard[row_idx - 1][square_idx - 1] = 1
            else:
                newBoard[row_idx - 1][square_idx - 1] = 0
    return board_to_tuple(newBoard)


def printBoard(gameBoard: tuple):
    """ Print the currnet board """
    print(f'{loc_cursor(1, 1)}Conway\'s Game of Life - Coded by: Preocts')
    open_ = colorama.Fore.WHITE + colorama.Back.BLACK
    close_ = colorama.Fore.WHITE + colorama.Back.RED
    gamepiece = '░'
    for ri, row in enumerate(gameBoard):
        for si, square in enumerate(row):
            if square:
                print(f'{close_}{gamepiece}', end='')
                # print(f' {close_}{si},{ri}', end='')
            else:
                print(f'{open_}{gamepiece}', end='')
                # print(f' {open_}{si},{ri}', end='')
        print('')
    return


def saveBoard(gameBoard: tuple, filename: str = 'gameboard.txt'):
    """ Saves state to file """
    with open(filename, 'w') as outfile:
        for row in gameBoard:
            for square in row:
                outfile.write(str(square))
            outfile.write('\n')
    return


def loadBoard(filename: str = 'gameboard.txt') -> tuple:
    """ Loads state to memory """
    gameBoard = []
    with open(filename, 'r') as infile:
        for line in infile:
            boardRow = []
            for char in line:
                if char == '\n':
                    continue
                boardRow.append(int(char))
            gameBoard.append(boardRow.copy())
    return board_to_tuple(gameBoard)


def life_count(gameBoard: tuple, x_idx: int, y_idx: int) -> int:
    """ Returns the number of living neighbors """
    counter = 0
    for x_move in range(-1, 2):
        for y_move in range(-1, 2):
            if x_move or y_move:
                counter += get_piece(gameBoard, x_idx + x_move, y_idx + y_move)
    return counter


def get_piece(gameBoard: tuple, x: int, y: int) -> int:
    """ Returns the state of the given location """
    max_x = len(gameBoard[0]) - 1
    max_y = len(gameBoard) - 1

    # Check for wraps
    if x > max_x:
        x = x - max_x - 1
    if x < 0:
        x = max_x + x + 1
    if y > max_y:
        y = y - max_y - 1
    if y < 0:
        y = max_y + y + 1

    # print(x, y)
    return gameBoard[y][x]


def evolve_board(gameBoard: tuple) -> tuple:
    """ Applies the rules of Conway's Game of Life """
    """
    Conway's Rules of life:

    RULE ONE
    - Each dead cell adjacnent to exactly three live neighbords will become
    live in the next generation

    RULE TWO
    - Each live cell with one or fewer live neighbords will die in the
    next generation.

    RULE THREE
    - Each live cell with four or more live neighbords will die in the
    next generation.

    RULE FOUR
    - Each live cell with either two or three live neighbors will remain
    alive for the next generation.
    """
    newBoard = board_to_list(gameBoard)

    for r_idx, row in enumerate(gameBoard):
        for cell_idx, square in enumerate(row):
            lifeCount = life_count(gameBoard, cell_idx, r_idx)
            # Rule One - Birth
            if lifeCount == 3:
                newBoard[r_idx][cell_idx] = 1  # You live
                continue
            # No other rule applies to dead cells
            if not(square):
                continue

            # Rule Two - Lonely
            if lifeCount <= 1:
                newBoard[r_idx][cell_idx] = 0  # You died
                continue

            # Rule Three - Overcrowded
            if lifeCount >= 4:
                newBoard[r_idx][cell_idx] = 0  # You died
                continue

            # Rule Four - Stable
            newBoard[r_idx][cell_idx] = square  # Nothing exciting
    # exit()
    return board_to_tuple(newBoard)


def scan_for_change(oldBoard: tuple, gameBoard: tuple) -> bool:
    """ Look for changes in life """

    for rows in zip(oldBoard, gameBoard):
        for values in zip(rows[0], rows[1]):
            if values[0] != values[1]:
                return True
    return False


def board_to_tuple(gameBoard: list) -> tuple:
    """ Converts rows to tuples """
    newBoard = []
    for row in gameBoard:
        newBoard.append(tuple(row))
    return tuple(newBoard)


def board_to_list(gameBoard: tuple) -> list:
    """ Converts rows to lists """
    newBoard = []
    for row in gameBoard:
        newBoard.append(list(row))
    return newBoard


def loc_cursor(x: int, y: int) -> str:
    return f"\033[{y};{x}f"


if __name__ == '__main__':
    colorama.init(autoreset=True)
    clearScreen()
    random.seed()
    gameBoard = assembleBoard(40, 20)
    oldBoard = gameBoard
    gameBoard = seedBoard(gameBoard, 62)
    # saveBoard(gameBoard)
    # gameBoard = loadBoard('pulsar.txt')
    counter = 0
    max_run = -1
    pause_time = .1

    while scan_for_change(oldBoard, gameBoard):
        printBoard(gameBoard)
        if max_run > 0 and counter > max_run:
            break
        print(f'Stage {counter}: {pause_time} seconds to next stage.')
        time.sleep(pause_time)
        oldBoard = gameBoard
        counter += 1
        gameBoard = evolve_board(gameBoard)

    print('\nThe game has concluded.')
    if counter < max_run:
        print('Life has either stagnated or perished.')
    else:
        print('Life has existed and grown')
    print(f'This ran for {counter} evolution cycles.')
    print('\n\nEnd. Of. Line.')
