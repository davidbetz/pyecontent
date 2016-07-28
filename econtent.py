import sys, os
import re
import datetime

def normalize_text(text):
    return text

def read(input):
    obj = { }
    body = []
    index = 0
    section_data = None
    content = {}
    for line in input.split('\n'):
        if len(line) == 0:
            continue
        if line.startswith('@@'):
            if line.startswith('@@begin|'):
                sr = re.search("@@begin\|(?P<type>[0-9a-zA-Z_]+)\:(?P<code>[0-9a-zA-Z_]+)@@", line)
                if sr != None:
                    type = sr.group(1)
                    code = sr.group(2)
                    content[index] = '\n'.join(body)
                    index = index + 1
                    body = []
                    section_data = { 'type': type, 'code': code }
            elif line == '@@end@@' and section_data != None:
                content[index] = {
                    section_data['type']: section_data['code'],
                    '_': normalize_text('\n'.join(body))
                }
                index = index + 1
                body = []
                section_data = None
        elif line[0] == '@':
            sr = re.search("^@(?P<type>[0-9a-zA-Z_\|]+)@(?P<content>.*)", line)
            if sr != None:
                obj[sr.group(1)] = sr.group(2).strip()
        else:
            sr = re.search("@@(?P<type>[0-9a-zA-Z_]+)\|(?P<code>[0-9a-zA-Z_]+)@@", line)
            if sr != None:
                type = sr.group(1)
                code = sr.group(2)
                ##+ don't really do anything; just good to know about

            body.append(line)

    content[index] = normalize_text('\n'.join(body))

    obj['_'] = content

    return obj

def read_file(path):
    with open(path, 'r') as f:
        obj = read(f.read())

    file_data = os.stat(path)

    if 'created' not in obj:
        obj['created'] = datetime.datetime.fromtimestamp(file_data.st_ctime).replace(microsecond=0).isoformat() + 'Z'

    if 'modified' not in obj:
        obj['modified'] = datetime.datetime.fromtimestamp(file_data.st_mtime).replace(microsecond=0).isoformat() + 'Z'

    obj['filename'] = os.path.basename(path)

    part_array = os.path.splitext(obj['filename'])
    obj['extension'] = part_array[1] if part_array[1][0] != '.' else part_array[1][1:]
    obj['basename'] = part_array[0]

    return obj