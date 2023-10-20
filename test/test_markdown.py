import unittest
from utilities import get_data, markdown


class MyTestCase(unittest.TestCase):
    def test_something(self):
        word= get_data.Word("liberate")
        text= markdown.word_markdown(word)
        print(text)
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
