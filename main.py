import argparse
import re

from Cube import Cube

import visu.visualizer as visu

def check_integrity(mix):
    regex = re.compile('^[FRUBLD]\'?[0-9]*$')
    final = []

    for token in filter(None, mix.split()):
        if not regex.match(token):
            print(f'Invalid token "{token}"')
            return
        final.append(token)
    if not final:
        print(f'Empty mix')
    return final

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Solve a rubik's cube")

    parser.add_argument('mix', type=str, help="Initial mix of the rubkik's cube")
    parser.add_argument('-v', dest='verbose', action='store_true', help='Verbose mode')
    parser.add_argument('-g', dest='graphics', action='store_true', help='Graphical mode')
    parser.add_argument('-r', metavar='RAND_LENGTH', type=int, dest='rand', help="Randomly generate RAND_LENGTH mix to apply to the rubik'scube")

    args = parser.parse_args()

    mix = check_integrity(args.mix)
    if not mix:
        exit(1)

    c = Cube()
    for i in c.cube:
        print(c.cube[i], c.cube[i].BASE_COLOR)
    c.twist('F', True)
    if args.graphics:
        visu.init(c)
