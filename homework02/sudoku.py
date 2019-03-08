import random
from typing import *


def read_sudoku(filename: str) -> list:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values: list) -> None:
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: list, n: int) -> list:
    """ Сгруппировать значения values в список, состоящий из списков по n элементов """
    """
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    grp = [values[x: x + n] for x in range(0, len(values), n)]
    return grp


def get_row(values: list, pos: tuple) -> list:
    """ Возвращает все значения для номера строки, указанной в pos """
    """
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return values[pos[0]]


def get_col(values: list, pos: tuple) -> list:
    """ Возвращает все значения для номера столбца, указанного в pos """
    """
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [col[pos[1]] for col in values]


def get_block(values: list, pos: tuple) -> list:
    """ Возвращает все значения из квадрата, в который попадает позиция pos """
    """"
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    row = row // 3
    col = col // 3
    total = []
    for num in values[row * 3: row * 3 + 3]:
        total += num[col * 3: col * 3 + 3]
    return total


def find_empty_positions(grid: list) -> Union[tuple, None]:
    """ Найти первую свободную позицию в пазле """
    """
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for row, values in enumerate(grid):
        for col, nums in enumerate(values):
            if nums == '.':
                return row, col
    return None


def find_possible_values(grid: list, pos: tuple) -> set:
    """ Вернуть множество возможных значения для указанной позиции """
    """
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    possible = set('123456789')
    all_row = set(get_row(grid, pos))
    all_col = set(get_col(grid, pos))
    all_block = set(get_block(grid, pos))
    return possible - all_row - all_col - all_block


def solve(grid: list) -> Union[list, None]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    empty = find_empty_positions(grid)
    if not empty:
        return grid
    row, col = empty
    for num in find_possible_values(grid, empty):
        grid[row][col] = num
        solution = solve(grid)
        if solution:
            return solution
    grid[row][col] = '.'
    return None


def check_solution(solution: list) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    for row in solution:
        if set(row) != set('123456789'):
            return False
    for col in range(len(solution)):
        if set(get_col(solution, (0, col))) != set('123456789'):
            return False
    for row, values in enumerate(solution):
        for col, nums in enumerate(values):
            pos = (row, col)
            if set(get_block(solution, pos)) != set('123456789'):
                return False
    return True


def generate_sudoku(N: int) -> list:
    """ Генерация судоку заполненного на N элементов """
    """
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    N = 81 - N
    grid = [['.'] * 9 for _ in range(9)]
    grid = solve(grid)
    while N > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if grid[row][col] != '.':
            grid[row][col] = '.'
            N -= 1
    return grid


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)