## copyright (c) 2016 David Betz

import os
import re
import datetime

def read(input):
    obj = { }
    body = []
    index = 0
    section_data = None
    content = {}
    format_content = None
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

                    format_index = 0
                    format_content = {}
            elif section_data is not None and line.startswith('@@'):
                if line == '@@end@@':
                    if format_content is None:
                        content[index] = {
                            section_data['type']: section_data['code'],
                            '_': '\n'.join(body)
                        }
                    else:
                        format_content[format_index] = {
                            section_data['type']: section_data['code'],
                            '_': '\n'.join(body)
                        }
                        content[index] = format_content

                    index = index + 1
                    body = []
                    section_data = None
                    format_content = None
                else:
                    sr = re.search("^@@(?P<type>[0-9a-zA-Z_]+)\:(?P<code>[0-9a-zA-Z_]+)@@", line)
                    if sr != None:
                        type = sr.group(1)
                        code = sr.group(2)
                        if format_content is None:
                            format_content = {}
                            format_index = 0
                        format_content[format_index] = {
                            section_data['type']: section_data['code'],
                            '_': '\n'.join(body)
                        }
                        section_data = { 'type': type, 'code': code }
                        format_index = format_index + 1
                        body = []

        elif line[0] == '@':
            sr = re.search("^@(?P<type>[0-9a-zA-Z_\|]+)@(?P<content>.*)", line)
            if sr != None:
                tag_type = sr.group(1)
                tag_content = sr.group(2).strip()
                if '|' in tag_type:
                    (bar_left, bar_right) = tag_type.split('|', 1)
                    obj[bar_left] = {
                        bar_right: tag_content
                    }
                else:
                    #+ don't save most stuff with prefix; it's my universal code for disabled (or system)
                    #+   it's VERY common to overwrite _created and _modified (since they are often killed
                    #+   when they go across FTP; but you can't mess with immutable stuff (e.g. filename)
                    if not tag_type.startswith('_') or tag_type in ('_created', '_modified'):
                        obj[tag_type] = tag_content
        else:
            sr = re.search("@@(?P<type>[0-9a-zA-Z_]+)\|(?P<code>[0-9a-zA-Z_]+)@@", line)
            if sr != None:
                type = sr.group(1)
                code = sr.group(2)
                ##+ don't really do anything; just good to know about

            body.append(line)

    if len(body) > 0:
        content[index] = '\n'.join(body)
        obj['_'] = content

    return obj


def read_file(path):
    with open(path, 'r') as f:
        obj = read(f.read())

    file_data = os.stat(path)

    #+ due to a file system design flaw, not all file systems have a file created date
    if '_created' not in obj:
        obj['_created'] = datetime.datetime.fromtimestamp(file_data.st_ctime).replace(microsecond=0).isoformat() + 'Z'

    if '_modified' not in obj:
        obj['_modified'] = datetime.datetime.fromtimestamp(file_data.st_mtime).replace(microsecond=0).isoformat() + 'Z'

    obj['_filename'] = os.path.basename(path)

    part_array = os.path.splitext(obj['_filename'])

    if len(part_array[1]) == 0:
        obj['_extension'] = part_array[0][1:]
        obj['_basename'] = ''
    else:
        obj['_extension'] = part_array[1] if part_array[1][0] != '.' else part_array[1][1:]
        obj['_basename'] = part_array[0]

    return obj