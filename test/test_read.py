import unittest, read


class ReadTestCase(unittest.TestCase):

    def test_read_from_files(self):
        path = "test.txt"
        words = read.read_words("file", path=path,filetype="foxitPDF")
        print(words)
        self.assertIn("synergy", words, "Read form files test failed")

if __name__ == '__main__':
    unittest.main()
