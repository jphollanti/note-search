import sys
import colorama
from colorama import Fore, Back
from pathlib import Path
import os

notes = '/Users/juha/notebooks/'

colorama.init()
SECTION = Back.LIGHTBLACK_EX
SECTION_NC = Back.RESET
HL = Fore.CYAN
NC = Fore.RESET

topic_colors = [Back.CYAN, Back.MAGENTA, Back.YELLOW, Back.GREEN, Back.BLUE]
used_colors = {}

ignore_dirs = ['template']
include_only = None


def get_dirs(path):
    dirs = []
    while 1:
        path, folder = os.path.split(path)
        if folder != "":
            dirs.append(folder)
        else:
            if path != "":
                dirs.append(path)
            break
    dirs.reverse()
    return dirs


def main(find):
    color_i = -1
    for path in Path(notes).glob('*/README.md'):
        identifier = get_dirs(path)[-2]
        if identifier in ignore_dirs:
            continue
        if include_only and identifier != include_only:
            continue
        color_i = color_i + 1
        if color_i > len(topic_colors) - 1:
            color_i = 0
        color = topic_colors[color_i]
        if color in used_colors:
            used_colors[color].append(identifier)
        else:
            used_colors[color] = [identifier]
        line_start = color + ' ' + SECTION_NC + ' ' if not include_only else ''
        found_something = False

        with open(path) as fp:
            section = ''
            line = fp.readline()
            do_print = find is None  # find nothing, print all
            while line:
                if line.startswith('# '):
                    if do_print:
                        print(section + line_start)
                    do_print = find is None  # find nothing, print all

                if find and find.lower() in line.lower():
                    idx = line.lower().find(find.lower())
                    while idx > -1:
                        p1 = line[:idx]
                        p2 = line[idx:idx + len(find)]
                        p3 = line[idx + len(find):]
                        p1 += HL
                        p3 = NC + p3
                        line = p1 + p2 + p3
                        idx = line.lower().find(find.lower(), idx + len(find) + len(HL) + len(NC))

                    do_print = True
                    found_something = True

                if line.startswith('# '):
                    section = line_start + SECTION + line.rstrip() + SECTION_NC + '\n'
                else:
                    # indent content of a section
                    section += line_start + '  ' + line

                line = fp.readline()

            if do_print:
                print(section + line_start)

        if found_something:
            print(line_start)
            print('')

    if not include_only:
        print('')
        print('Legend:')
        for key, value in used_colors.items():
            print(' ' + key + '  ' + SECTION_NC + ' = ' + ', '.join([str(elem) for elem in value]))


if __name__ == "__main__":
    print('')
    find = None
    if len(sys.argv) > 1:
        find = sys.argv[1]
    # if len(sys.argv) > 2:
    #     for ignore in sys.argv[2:]:
    #         ignore_dirs.append(ignore)
    if len(sys.argv) > 2:
        include_only = sys.argv[2]
    main(find)
