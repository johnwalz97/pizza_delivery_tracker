from argparse import ArgumentParser
from itertools import cycle
from math import ceil, sqrt
from pathlib import Path
from typing import List, Tuple

import numpy as np


def preprocess(moves: str) -> str:
    """
    Takes a string of dispatcher inputs (^, v, <, >) and removes leading and trailing whitespace, quotes and newlines

    :param moves: string containing dispatcher inputs
    :return: processed moves
    """
    moves = moves.strip()
    moves = moves.strip('\'')
    moves = moves.strip('\n')

    return moves


def validate_moves(moves: str):
    """
    Takes a string of dispatcher inputs and validates that it contains only valid moves

    :param moves: string containing dispatcher inputs
    :raises ValueError: raises exception if the string contains invalid move character
    """
    for move in moves:
        if move not in ['^', 'v', '>', '<']:
            raise ValueError('Invalid move passed. Must be ^, v, <, or >')


def vectorize_moves(moves: str) -> List[np.ndarray]:
    """
    Takes a string of dispatcher inputs and translates them into numpy vectors that can
    be more efficiently processed.

    :param moves: string containing dispatcher inputs
    :return: list of moves as numpy vectors
    """
    moves_map = {
        '^': np.array([0, 1]),
        'v': np.array([0, -1]),
        '>': np.array([1, 0]),
        '<': np.array([-1, 0]),
    }

    return [moves_map[move] for move in moves]


def track_deliveries(
        vectors: List[np.ndarray],
        num_agents: int = 1,
        calculate_grid: bool = True,
) -> Tuple[np.ndarray, Tuple[List, List]]:
    """
    Iterates through the list of moves which have been vectorized. Tracks house coordinates visited and optionally
    tracks the min and max x,y coordinates that describe a diagonal for a square 2d grid which can contain all the
    deliveries.

    :param vectors: list of vectorized moves to iterate through
    :param num_agents: number of delivery agents (agents take turns doing deliveries)
    :param calculate_grid: flag specifying whether or not to calculate the grid diagonal
    :return: tuple containing the positions visited as well as the coordinates for the grid diagonal
    """
    agents = cycle(range(num_agents))
    agent_positions = [np.array([0, 0]) for _ in range(num_agents)]

    deliveries = np.ndarray((len(vectors) + 1, 3))
    deliveries[0] = np.array([0, 0, 0])

    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    for i, move in enumerate(vectors, start=1):
        current_agent = next(agents)

        # have the current agent perform the next move (add move vector to agent's position)
        agent_positions[current_agent] += move
        current_position = agent_positions[current_agent]

        # add delivery coordinates and current agent index into the list of all deliveries
        deliveries[i] = np.append(current_position, current_agent)

        # all this does is check if the current position is farther out on the grid than
        # any of the previous deliveries and if it is it updates the max or min x,y coords
        if calculate_grid:
            if current_position[0] < min_x:
                min_x = current_position[0]
            if current_position[0] > max_x:
                max_x = current_position[0]
            if current_position[1] < min_y:
                min_y = current_position[1]
            if current_position[1] > max_y:
                max_y = current_position[1]

    return deliveries, ([min_x, min_y], [max_x, max_y])


def process_moves(
        moves_str: str = None,
        moves_file: Path = None,
        num_agents: int = 1,
        calculate_grid: bool = True,
) -> Tuple[int, np.ndarray, Tuple[List, List]]:
    """
    Main function for processing dispatcher inputs. Takes either a string of moves or a file path
    as the input, as well as a boolean specifying whether or not to calculate the diagonal for  a
    square 2d grid that can contain all the moves. This diagonal measurement can be used to draw a
    grid and animate the moves within it.

    :param moves_str: string of dispatcher inputs
    :param moves_file: file path pointing to flat text file containing dispatcher inputs
    :param num_agents: number of agents that will be delivering pizzas (agents take turns doing deliveries)
    :param calculate_grid: indicates whether or not to calculate grid diagonal - Useful for large
                           inputs when the diagonal is not required, as this can save some processing time.
    :return: tuple containing the number of unique houses visited, the positions visited as well as the
             coordinates for the grid diagonal
    """

    if moves_file:
        with open(moves_file) as fd:
            lines = fd.readlines()

        moves = "".join([preprocess(line) for line in lines])

    elif moves_str:
        moves = preprocess(moves_str)

    else:
        raise Exception("No moves to process. Must pass either moves_str or moves_file as input")

    validate_moves(moves)
    vectorized_moves = vectorize_moves(moves)

    deliveries, diagonal = track_deliveries(vectorized_moves, num_agents, calculate_grid)

    return len(np.unique(deliveries[:, :2], axis=0)), deliveries, diagonal


if __name__ == '__main__':
    help_text = '''
    This python script takes dispatcher inputs (^, v, <, >) and uses them to track pizzas delivered.
    When called with the --moves-file argument it expects a flat text file with valid moves that. If called with
    no arguments it will prompt user to type in moves to be processed.
    '''
    parser = ArgumentParser(description=help_text)
    parser.add_argument('--moves-file', help='flat text file containing only valid dispatcher inputs', type=Path)
    parser.add_argument('--agents', default=1, help='number of delivery agents', type=int)
    args = parser.parse_args()

    if args.moves_file:
        unique_houses, _, grid_diagonal = process_moves(moves_file=args.moves_file, num_agents=args.agents)
    else:
        raw_input = input('Enter the list of moves: ')
        unique_houses, _, grid_diagonal = process_moves(moves_str=raw_input, num_agents=args.agents)

    grid_diagonal_length = ceil(sqrt(
        (grid_diagonal[1][0] - grid_diagonal[0][0]) ** 2 +
        (grid_diagonal[1][1] - grid_diagonal[0][1]) ** 2
    ))

    print(f'Number of unique house visited: {unique_houses}')
    print(f'Grid diagonal coordinates: {grid_diagonal[0]} {grid_diagonal[1]}')
    print(f'Grid diagonal length: {grid_diagonal_length}')
