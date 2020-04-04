import sys
import colorama
from colorama import Fore, Back

notes = '/Users/juha/notebooks/system/README.md'

colorama.init()
SECTION = Back.LIGHTBLACK_EX
SECTION_NC = Back.RESET
HL = Fore.CYAN
NC = Fore.RESET


def main(find):
    with open(notes) as fp:
        section = ''
        line = fp.readline()
        do_print = find is None  # find nothing, print all
        while line:
            if line.startswith('# '):
                if do_print:
                    print(section)
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

            if line.startswith('# '):
                section = SECTION + line.rstrip() + SECTION_NC + '\n'
            else:
                # indent content of a section
                section += '  ' + line

            line = fp.readline()

        if do_print:
            print(section)


if __name__ == "__main__":
    print('')
    find = None
    if len(sys.argv) > 1:
        find = sys.argv[1]
    main(find)
