import sys
import colorama
from colorama import Fore, Back
from pathlib import Path
import os
import tempfile
import base64

config = {}
config_fn = os.path.expanduser('~') + '/.note-search.cfg'

with open(config_fn) as f:
    for line in f:
        if line.startswith('#'):
            continue
        if '=' in line:
            name, value = line.split('=', 1)
            config[name.strip()] = value.strip()

print("Using config: ")
print(config) 

colorama.init()
SECTION = Back.LIGHTBLACK_EX
SECTION_NC = Back.RESET
HL = Fore.CYAN
NC = Fore.RESET

topic_colors = [Back.CYAN, Back.MAGENTA, Back.YELLOW, Back.GREEN, Back.BLUE]
used_colors = {}

ignore_dirs = config['IGNORE_DIRS'].split(',')
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
    for path in Path(config['NOTES_DIR']).glob('*/README.md'):
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

        ## base64decode hush file, write to temp file, use that file instead
        if identifier == 'hush':
            with open(path) as f:
                data = f.read()
            clrtxt = base64.b64decode(data).decode("ascii")
            fd, path2 = tempfile.mkstemp()
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(clrtxt)
            path = path2

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
                    if not found_something and not include_only:
                        print(color + ' ' * 5 + identifier + ' ' * 5 + SECTION_NC)
                        print(line_start)
                    found_something = True

                if line.startswith('# '):
                    section = line_start + SECTION + line.rstrip() + SECTION_NC + '\n'
                else:
                    # indent content of a section
                    section += line_start + '  ' + line

                line = fp.readline()

            if do_print:
                print(section + line_start)

        if identifier == 'hush':
            # remove temp file
            os.remove(path)
        
        # if found_something:
        #     #print(line_start)
        #     if not include_only:
        #         print(color + ' ' * 15 + SECTION_NC)

            print('')

    if not include_only:
        print('')
        print('Legend:')
        for key, value in used_colors.items():
            print(' ' + key + '  ' + SECTION_NC + ' = ' + ', '.join([str(elem) for elem in value]))
        print('')


if __name__ == "__main__":
    print('')
    find = None

    aa = []

    exclude_hush = True
    for arg in sys.argv:
        if arg == '+hush':
            exclude_hush = False
            break
        else: 
            aa.append(arg)
    if exclude_hush:
        ignore_dirs.append('hush')


    if len(aa) > 1:
        find = aa[1]
    # if len(sys.argv) > 2:
    #     for ignore in sys.argv[2:]:
    #         ignore_dirs.append(ignore)
    if len(aa) > 2:
        include_only = aa[2]
    main(find)
