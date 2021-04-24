# MIT License

# Copyright (c) 2016-2021 David Betz

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
            body.append(line)
            continue
        line_handled = False
        if line.startswith('@@'):
            if line.startswith('@@begin|'):
                line_handled = True
                sr = re.search("@@begin\|(?P<type>[0-9a-zA-Z_]+)\:(?P<code>[0-9a-zA-Z_]+)@@", line)
                if sr != None:
                    type = sr.group(1)
                    code = sr.group(2)
                    content[index] = '\n'.join(body).strip("\n")
                    index = index + 1
                    body = []
                    section_data = { 'type': type, 'code': code }

                    format_index = 0
                    format_content = {}
            elif section_data is not None and line.startswith('@@'):
                line_handled = True
                if line == '@@end@@':
                    if format_content is None:
                        content[index] = {
                            section_data['type']: section_data['code'],
                            '_': '\n'.join(body).strip("\n")
                        }
                    else:
                        format_content[format_index] = {
                            section_data['type']: section_data['code'],
                            '_': '\n'.join(body).strip("\n")
                        }
                        content[index] = format_content

                    index = index + 1
                    body = []
                    section_data = None
                    format_content = None
                else:
                    line_handled = True
                    sr = re.search("^@@(?P<type>[0-9a-zA-Z_]+)\:(?P<code>[0-9a-zA-Z_]+)@@", line)
                    if sr != None:
                        type = sr.group(1)
                        code = sr.group(2)
                        if format_content is None:
                            format_content = {}
                            format_index = 0
                        format_content[format_index] = {
                            section_data['type']: section_data['code'],
                            '_': '\n'.join(body).strip("\n")
                        }
                        section_data = { 'type': type, 'code': code }
                        format_index = format_index + 1
                        body = []

            if not line_handled:
                # this allows for @@asdfasdf@@ to start a line; meaning @@footnote@@ can start a line
                body.append(line)
                
        elif line[0] == '@':
            sr = re.search("^@(?P<type>[0-9a-zA-Z_\|]+)@(?P<content>.*)", line)
            if sr != None:
                tag_type = sr.group(1)
                tag_content = sr.group(2).strip()
                if '|' in tag_type:
                    (bar_left, bar_right) = tag_type.split('|', 1)
                    if bar_left not in obj:
                        obj[bar_left] = {}
                    obj[bar_left][bar_right] = tag_content
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
        content[index] = '\n'.join(body).strip("\n")
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