from flask import Flask, request, jsonify, send_from_directory

from flask_cors import CORS
from pathlib import Path
import os


app = Flask(__name__, static_folder='public')
CORS(app)  # Enable CORS


config = {}

if 'NOTES_CONFIG_FILE' in os.environ:
    config_fn = os.environ['NOTES_CONFIG_FILE']
else:
    config_fn = os.path.expanduser('~') + '/.note-search.cfg'

with open(config_fn) as f:
    for line in f:
        if line.startswith('#'):
            continue
        if '=' in line:
            name, value = line.split('=', 1)
            config[name.strip()] = value.strip()

# override with env vars
if 'NOTES_DIR' in os.environ:
    config['NOTES_DIR'] = os.environ['NOTES_DIR']

print("Using config: ")
print(config) 

ignore_dirs = config['IGNORE_DIRS'].split(',')
include_only = None



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print("serving: " + path, app.static_folder + '/' + path)
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    #filtered_items = [item for item in items if query in item.lower()]
    #return jsonify(filtered_items)
    return __find(query)
    

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


def __find(find):
    """
    Find a string in all notes
    TODO: add hush
    """
    results = []

    print(config['NOTES_DIR'], find)

    for path in Path(config['NOTES_DIR']).glob('*/README.md'):
        print("processing: " + str(path))
        identifier = get_dirs(path)[-2]
        if identifier in ignore_dirs:
            continue
        if include_only and identifier != include_only:
            continue
        
        section = {
            'path': str(path), 
            'topics': []
        }

        with open(path) as fp:
            topic = {'header': None, 'content': ''}
            line = fp.readline()
            found_match_in_section = False

            while line:
                if line.startswith('# '):
                    if topic['header'] and found_match_in_section:
                        section['topics'].append(topic)
                    
                    # start processing new section
                    topic = {'header': None, 'content': ''}
                    topic['header'] = line.rstrip()[2:]
                    found_match_in_section = False
                else:
                    # indent content of a section
                    topic['content'] += line
                
                if find and find.lower() in line.lower():
                    idx = line.lower().find(find.lower())
                    if idx > -1:
                        found_match_in_section = True
                        print("Found match in " + str(path))
                    

                line = fp.readline()
            
            if topic['header'] and found_match_in_section:
                section['topics'].append(topic)

        
        if len(section['topics']) > 0:
            results.append(section)

    return results


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)
