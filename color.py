#! /usr/bin/env python

import random
import sys
from timeit import default_timer as timer


def random_square():
    return "%s%d" % ("abcdefgh"[random.randint(0, 7)], random.randint(1, 8))


def color(square):
    return ["w", "b"][(ord(square[0]) - ord("a") + int(square[1])) % 2]


def interactive_color():
    correct = 0
    bad = 0
    play = True
    elapsed = 0
    avg_elapsed = 0
    questions = 0

    while play:
        square = random_square()

        start = timer()
        result = ""
        while result not in ["w", "b", "q"]:
            print("Color for %s (w/b/q)?" % square)
            result = sys.stdin.readline().rstrip()

        if result == "q":
            play = False
            print("-> You answered %.d%% correctly (avg %.d ms)" % ((correct/(correct+bad))*100, avg_elapsed*1000))
        else:
            elapsed = timer() - start
            total_elapsed = avg_elapsed * questions + elapsed
            questions += 1
            avg_elapsed = total_elapsed/questions

            if result == color(square):
                correct += 1
                print("-> Correct! (%.d ms)\n" % (elapsed*1000))
            else:
                bad += 1
                print("-> Bad! (%.d ms)\n" % (elapsed*1000))


if __name__ == "__main__":
    interactive_color()
