# MIT License

# Copyright (c) 2016-2017 David Betz

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

import unittest

import os

try:
    import econtent
except:
    from . import econtent

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
SAMPLE_PATH = os.path.join(CURRENT_PATH, 'sample')
ITEM01_PATH = os.path.join(SAMPLE_PATH, 'item01.txt')
ITEM02_PATH = os.path.join(SAMPLE_PATH, 'item02.md')
ITEM03_PATH = os.path.join(SAMPLE_PATH, 'item03.md')
MANIFEST_PATH = os.path.join(SAMPLE_PATH, '.manifest')

ITEM01_EXPECTED = {
    '_': {
        0: 'hollow unbraced needs mineral high fingerd strings red tragical having definement invisible@@footnote|78@@. flames grow pranks obey hearsed variable grandsire bodykins possessd worser oerthrown oerweigh healthful kingly wise faculty loggats best.\n\nunfortified chopine hill witchcraft@@note|holds@@ countries toward nerve grief duty rivals.',
        1: {
            0: {
                '_': "    alert((function() {\n      var item = 'item01';\n      return item.split('').reverse()\n    })());",
                'format': 'javascript'
            },
            1: {
                '_': "    print('item01'[::-1])",
                'format': 'python'
            }
        },
        2: 'patience unhouseld pours lapsed would passion@@note|upshot@@ point blastments lady spectators.@@footnote|99@@',
    },
    'author': 'Billy Speareshakes',
    'title': 'Thy Wonderful Randomious',
    'page': '728',
    'footnote': {
        "78": 'nose thee something disclaiming wrung antiquity rend illume halt osric list',
        "99": 'unclefather concernings customary',
    },
    'note': {
        "holds": 'forgery chanson',
        "upshot": 'thoroughly served fame',
    },
    '_created': '2016-07-27T19:38:10Z',
    '_modified': '2016-07-27T19:38:10Z',
    '_filename': 'item01.txt',
    '_extension': 'txt',
    '_basename': 'item01',
}

MANIFEST_EXPECTED = {
    'author': 'Billy Speareshakes',
    'title': 'Thy Wonderful Randomious',
    'page': '728',
    '_created': '2016-07-27T19:38:10Z',
    '_modified': '2016-07-27T19:38:10Z',
    '_filename': '.manifest',
    '_extension': 'manifest',
    '_basename': '',
}

ITEM02_EXPECTED={
    'citation': 'Gary the Snail. Spongebob.',
     '_': {
         0: 'There once was a man from Peru\n\nwho dreamt of eating his shoe\n\nhe woke with a fright in the middle of the night\n\nto find his dream had come true'
        },
    "_created": "2021-04-24T17:04:57Z",
    "_modified": "2021-04-24T17:04:57Z",
    "_filename": "item02.md",
    "_extension": "md",
    "_basename": "item02"
}

ITEM03_EXPECTED={
    '_': {
        0:
        'patient mattering graves breathes six endure appeard longermarried infusion lover count digged abridgement dread profoundest:',
        1: {
            0: {
                'insert': 'entry',
                '_': 'perchance/therein'
            }
        },
        2:
        'drinks\n\n@@footnote|perchance@@\n\ntill translate weaker perfections hearers comest pitied redeliver insolence'
    }
}

class TestApp(unittest.TestCase):
    def disabled_test_walk(self):
        """
        for multi-file development
        """
        folder = '/home/dbetz/random'
        for f in os.listdir(folder):
            full = os.path.join(folder, f)
            try:
                result = econtent.read_file(full)
            except UnicodeDecodeError as err:
                print('cannot read {}'.format(full))
                print(err)
                continue

            print(result['basename'])


    def test_parse(self):
        with open(ITEM01_PATH, 'r') as f:
            result = econtent.read(f.read())
            self.check01(ITEM01_EXPECTED, result)

    def test_parse_file(self):
        result = econtent.read_file(ITEM01_PATH)

        self.check01(ITEM01_EXPECTED, result)
        self.check_file_data(ITEM01_EXPECTED, result)

    def test_parse_file2(self):
        result = econtent.read_file(ITEM02_PATH)

        self.assertEqual(ITEM02_EXPECTED['_'][0], result['_'][0])

    def test_parse_file3(self):
        result = econtent.read_file(ITEM03_PATH)

        self.assertEqual(ITEM03_EXPECTED['_'][0], result['_'][0])
        self.assertEqual(ITEM03_EXPECTED['_'][1][0]["insert"], result['_'][1][0]["insert"])
        self.assertEqual(ITEM03_EXPECTED['_'][1][0]["_"], result['_'][1][0]["_"])
        self.assertEqual(ITEM03_EXPECTED['_'][2], result['_'][2])

    def test_parse_manifest(self):
        result = econtent.read_file(MANIFEST_PATH)

        with self.assertRaises(KeyError):
            result['_']

        self.assertEqual(MANIFEST_EXPECTED['author'], result['author'])
        self.assertEqual(MANIFEST_EXPECTED['title'], result['title'])
        self.assertEqual(MANIFEST_EXPECTED['page'], result['page'])
        self.assertEqual(MANIFEST_EXPECTED['_created'], result['_created'])
        self.assertEqual(MANIFEST_EXPECTED['_modified'], result['_modified'])

        self.check_file_data(MANIFEST_EXPECTED, result)

    def check_file_data(self, expected, result):
        self.assertEqual(expected['_filename'], result['_filename'])
        self.assertEqual(expected['_extension'], result['_extension'])
        self.assertEqual(expected['_basename'], result['_basename'])


    def check01(self, expected, result):
        self.assertEqual(expected['_'][0], result['_'][0])
        self.assertEqual(expected['_'][1][0]['_'], result['_'][1][0]['_'])
        self.assertEqual(expected['_'][1][0]['format'], result['_'][1][0]['format'])
        self.assertEqual(expected['_'][1][1]['_'], result['_'][1][1]['_'])
        self.assertEqual(expected['_'][1][1]['format'], result['_'][1][1]['format'])
        self.assertEqual(expected['_'][2], result['_'][2])
        self.assertEqual(expected['author'], result['author'])
        self.assertEqual(expected['title'], result['title'])
        self.assertEqual(expected['page'], result['page'])
        self.assertEqual(expected['footnote']["78"], result['footnote']["78"])
        self.assertEqual(expected['footnote']["99"], result['footnote']["99"])
        self.assertEqual(expected['note']["holds"], result['note']["holds"])
        self.assertEqual(expected['note']["upshot"], result['note']["upshot"])
        self.assertEqual(expected['_created'], result['_created'])
        self.assertEqual(expected['_modified'], result['_modified'])


if __name__ == '__main__':
    unittest.main()
