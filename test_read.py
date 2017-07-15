import unittest

import os

import econtent

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
SAMPLE_PATH = os.path.join(CURRENT_PATH, 'sample')
ITEM01_PATH = os.path.join(SAMPLE_PATH, 'item01.txt')
MANIFEST_PATH = os.path.join(SAMPLE_PATH, '.manifest')

ITEM01_EXPECTED = {
    '_': {
        0: 'hollow unbraced needs mineral high fingerd strings red tragical having definement invisible@@footnote|78@@. flames grow pranks obey hearsed variable grandsire bodykins possessd worser oerthrown oerweigh healthful kingly wise faculty loggats best.\nunfortified chopine hill witchcraft countries toward nerve grief duty rivals.',
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
        2: 'patience unhouseld pours lapsed would passion point blastments lady spectators.',
    },
    'author': 'Billy Speareshakes',
    'title': 'Thy Wonderful Randomious',
    'page': '728',
    'footnote': {
        78: 'nose thee something disclaiming wrung antiquity rend illume halt osric list',
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
            self.check(ITEM01_EXPECTED, result)


    def test_parse_file(self):
        result = econtent.read_file(ITEM01_PATH)

        self.check(ITEM01_EXPECTED, result)
        self.check_file_data(ITEM01_EXPECTED, result)


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


    def check(self, expected, result):
        self.assertEqual(expected['_'][0], result['_'][0])
        self.assertEqual(expected['_'][1][0]['_'], result['_'][1][0]['_'])
        self.assertEqual(expected['_'][1][0]['format'], result['_'][1][0]['format'])
        self.assertEqual(expected['_'][1][1]['_'], result['_'][1][1]['_'])
        self.assertEqual(expected['_'][1][1]['format'], result['_'][1][1]['format'])
        self.assertEqual(expected['_'][2], result['_'][2])
        self.assertEqual(expected['author'], result['author'])
        self.assertEqual(expected['title'], result['title'])
        self.assertEqual(expected['page'], result['page'])
        self.assertEqual(expected['footnote'][78], expected['footnote'][78])
        self.assertEqual(expected['_created'], result['_created'])
        self.assertEqual(expected['_modified'], result['_modified'])


if __name__ == '__main__':
    unittest.main()
