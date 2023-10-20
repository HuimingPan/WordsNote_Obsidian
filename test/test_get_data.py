import unittest
from utilities import get_data

word = get_data.Word("engineering")


class MyTestCase(unittest.TestCase):
    def test_Word_get_page(self):
        word._get_page()
        self.assertIn("<!DOCTYPE html>", word.html, "_get_page failed")

    def test_Word_get_spelling(self):
        word._get_spelling()
        self.assertEqual("engineering", word.spelling, "_get_spelling test fail")

    def test_Word_get_phonetic(self):
        word._get_phonetic()
        self.assertEqual("/ˌɛndʒɪˈnɪərɪŋ/",word.phonetic, "_get_pronunciation test fail")

    def test_Word_get_rank(self):
        word._get_rank()
        self.assertEqual('CET4 TEM4',word.rank,"_get_rank test fail")

    def test_Word_get_explanations(self):
        word._get_explanations()
        trans_list=[
            {"property":"N-UNCOUNT",
             'meaning': '工程;工程学'
             "example_list":[
                 {"example_EN":" ...graduates with degrees in engineering. ",
                  "example_CN":"…获得工程学学位的毕业生。",
                }]}]
        self.assertEqual(trans_list,word.trans_list,"_get_explanations test fail")


if __name__ == '__main__':
    unittest.main()
