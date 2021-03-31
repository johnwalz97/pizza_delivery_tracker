from argparse import ArgumentParser


def format_moves(moves):
    moves = moves.strip()
    moves = moves.strip('\n')

    return moves


def track_deliveries(moves):
    current_position = (0, 0)
    houses_visited = set()

    for move in moves:
        if move == '>':
            current_position = ((current_position[0] + 1), current_position[1])
        elif move == '<':
            current_position = ((current_position[0] - 1), current_position[1])
        elif move == '^':
            current_position = (current_position[0], (current_position[1] + 1))
        elif move == 'v':
            current_position = (current_position[0], (current_position[1] - 1))
        else:
            raise Exception(f'Invalid move detected: {move}')

        houses_visited.add(current_position)

    return len(houses_visited), houses_visited


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--moves-file', help='file containing list of moves')
    args = parser.parse_args()

    if args.moves_file:
        with open(args.moves_file) as fd:
            raw_moves = fd.readlines()[0]
            dispatcher_inputs = format_moves(raw_moves)
    else:
        raw_moves = input('Enter the list of moves: ')
        dispatcher_inputs = format_moves(raw_moves)

    total, unique = track_deliveries(dispatcher_inputs)

    print(f'Number of unique house visited: {total}')
    print(unique)
