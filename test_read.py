import unittest

import sys, os

import econtent

current_path = os.path.dirname(os.path.realpath(__file__))
sample_path = os.path.join(current_path, 'sample')
item01_path = os.path.join(sample_path, 'item01.txt')

expected = {
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

class TestApp(unittest.TestCase):
    def disabled_test_walk(self):
        """
        for multi-file development
        """
        folder = '/home/dbetz/random'
        for file in os.listdir(folder):
            full = os.path.join(folder, file)
            try:
                result = econtent.read_file(full)
            except UnicodeDecodeError as err:
                print('cannot read {}'.format(full))
                print(err)
                continue

            print(result['basename'])

            log('content', result['_'][0])

    def test_parse(self):
        with open(item01_path, 'r') as f:
            result = econtent.read(f.read())
            self.check(result)

    def test_parse_file(self):
        result = econtent.read_file(item01_path)

        self.check(result)

        self.assertEqual(expected['_filename'], result['_filename'])
        self.assertEqual(expected['_extension'], result['_extension'])
        self.assertEqual(expected['_basename'], result['_basename'])

    def check(self, result):
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
