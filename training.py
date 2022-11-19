#! /usr/bin/env python

import argparse
import random
import sys
from timeit import default_timer as timer


COLORS = {
    'w': 'white',
    'b': 'black'
}

PIECES = {
    'K': 'king',
    'Q': 'queen',
    'R': 'rook',
    'B': 'bishop',
    'N': 'knight',
    '': 'pawn'
}


class Statistics:
    def __init__(self):
        self.average_elapsed = 0
        self.iterations = 0
        self.correct = 0
        self.bad = 0

    def add(self, elapsed, is_correct):
        total_elapsed = self.average_elapsed * self.iterations + elapsed
        self.iterations += 1
        self.average_elapsed = total_elapsed / self.iterations
        if is_correct:
            self.correct += 1
        else:
            self.bad += 1

    def get_correct_ratio(self):
        return self.correct / (self.correct + self.bad)

    def get_average_elapsed(self):
        return self.average_elapsed


def random_square():
    return to_square(random.randint(0, 7) + 1, random.randint(1, 8))


def random_piece():
    letter = random.choice(list(PIECES.keys()))
    color = random.choice(['w', 'b'])
    return letter, PIECES[letter], color


def color(square):
    return ["w", "b"][(ord(square[0]) - ord("a") + int(square[1])) % 2]


def to_coordinates(square):
    return ord(square[0]) - ord("a") + 1, int(square[1])


def to_square(x, y):
    return "%s%d" % ("abcdefgh"[x - 1], y)


def to_square_if_within_limits(x, y):
    if (1 <= x <= 8) and (1 <= y <= 8):
        return "%s%d" % ("abcdefgh"[x - 1], y)
    else:
        return None


def append_if_within_limits(destinations, piece_letter, x, y):
    square = to_square_if_within_limits(x, y)
    if square is not None:
        destinations.append(piece_letter + square)


def all_destinations(square, piece_letter, piece_color):
    x, y = to_coordinates(square)
    destinations = []
    if PIECES[piece_letter] == 'king':
        append_if_within_limits(destinations, piece_letter, x + 1, y)
        append_if_within_limits(destinations, piece_letter, x + 1, y - 1)
        append_if_within_limits(destinations, piece_letter, x, y - 1)
        append_if_within_limits(destinations, piece_letter, x - 1, y - 1)
        append_if_within_limits(destinations, piece_letter, x - 1, y)
        append_if_within_limits(destinations, piece_letter, x - 1, y + 1)
        append_if_within_limits(destinations, piece_letter, x, y + 1)
        append_if_within_limits(destinations, piece_letter, x + 1, y + 1)
    if PIECES[piece_letter] in ['queen', 'bishop']:
        d45 = min(8 - x, 8 - y)
        d135 = min(x - 1, 8 - y)
        d225 = min(x - 1, y - 1)
        d315 = min(8 - x, y - 1)
        for ii in range(1, d45 + 1):
            append_if_within_limits(destinations, piece_letter, x + ii, y + ii)
        for ii in range(1, d135 + 1):
            append_if_within_limits(destinations, piece_letter, x - ii, y + ii)
        for ii in range(1, d225 + 1):
            append_if_within_limits(destinations, piece_letter, x - ii, y - ii)
        for ii in range(1, d315 + 1):
            append_if_within_limits(destinations, piece_letter, x + ii, y - ii)
    if PIECES[piece_letter] in ['queen', 'rook']:
        for xx in range(1, x):
            append_if_within_limits(destinations, piece_letter, xx, y)
        for xx in range(x + 1, 9):
            append_if_within_limits(destinations, piece_letter, xx, y)
        for yy in range(1, y):
            append_if_within_limits(destinations, piece_letter, x, yy)
        for yy in range(y + 1, 9):
            append_if_within_limits(destinations, piece_letter, x, yy)
    if PIECES[piece_letter] == 'pawn' and piece_color == 'w':
        append_if_within_limits(destinations, piece_letter, x, y + 1)
    if PIECES[piece_letter] == 'pawn' and piece_color == 'b':
        append_if_within_limits(destinations, piece_letter, x, y - 1)

    return destinations

def training_color_iteration(statistics):
    square = random_square()

    start = timer()
    response = ""
    while response not in ["w", "b", "q"]:
        print("Color for %s (w/b/q)?" % square)
        response = sys.stdin.readline().rstrip()

    if response != "q":
        elapsed = timer() - start

        if response == color(square):
            statistics.add(elapsed, True)
            print("-> Correct! (%.d ms)\n" % (elapsed * 1000))
        else:
            statistics.add(elapsed, False)
            print("-> Bad! (%.d ms)\n" % (elapsed * 1000))

        return True
    else:
        print("-> You answered %.d%% correctly (avg %.d ms)" %
              (statistics.get_correct_ratio() * 100, statistics.get_average_elapsed() * 1000))
        return False


def training_color():
    statistics = Statistics()
    while training_color_iteration(statistics):
        pass


def training_piece_iteration(statistics):
    square = random_square()
    piece_letter, piece_name, piece_color = random_piece()
    destinations = all_destinations(square, piece_letter, piece_color)
    destinations.sort()

    start = timer()

    print("\nSquares for %s %s in %s (comma separated, q)?" % (COLORS[piece_color], piece_name, square))
    response = sys.stdin.readline().rstrip()

    if response != "q":
        elapsed = timer() - start
        response_destinations = response.split()
        response_destinations.sort()
        if response_destinations == destinations:
            statistics.add(elapsed, True)
            print("-> Correct! (%.d ms)\n" % (elapsed * 1000))
        else:
            statistics.add(elapsed, False)
            print("-> Bad! (%.d ms)\n" % (elapsed * 1000))
            print("-> Result: ", " ".join(destinations))
        return True
    else:
        print("-> You answered %.d%% correctly (avg %.d ms)" %
              (statistics.get_correct_ratio() * 100, statistics.get_average_elapsed() * 1000))
        return False


def training_piece():
    statistics = Statistics()
    while training_piece_iteration(statistics):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interactive training for chess')
    parser.add_argument('--training', choices=['color', 'piece'], help='Training type to follow')
    args = parser.parse_args()

    if args.training == 'color':
        training_color()
    elif args.training == 'piece':
        training_piece()
    else:
        parser.print_help()
