import urllib.request
from lxml import etree
import re


class Word:
    def __init__(self, word):
        self.spelling = word
        self._get_page()
        self._get_spelling()
        self._get_phonetic()
        self._get_rank()
        self._get_explanations()

    def _get_page(self):
        """
        Download the html page of the word from the Internet.
        """
        # url = f'https://youdao.com/result?word={self.spelling}&lang=en'
        # url = f'https://www.iciba.com/word?w={self.spelling}'
        # url = f'https://fanyi.sogou.com/text?keyword={self.spelling}%0A&transfrom=auto&transto=zh-CHS&model=general'
        self.url = f'https://dict.youdao.com/w/eng/{self.spelling}/'
        response = urllib.request.urlopen(self.url)
        self.html = response.read().decode('utf-8')
        self.selector = etree.HTML(self.html)

        self.collins_selector = self.selector.xpath('//*[@id="collinsResult"]/div/div/div/div')[0]

        print(f"No collins translation of {self.spelling}")

    def _get_spelling(self):
        """
        The spelling in the page is gotting in case of wrong spelling.
        """
        xpath = '//h4/span[@class="title"]'

        spelling_found = self.collins_selector.xpath(xpath)[0].text
        if spelling_found:
            if spelling_found == self.spelling:
                pass
            else:
                print("'{}' is not found, but {} is found" \
                      .format(self.spelling, spelling_found))
                self.spelling = spelling_found
        else:
            print("***'{}' is not found. It may be wrong and was omitted.***".format(self.spelling))

    def _get_phonetic(self):
        """
        Get the phonetic in the page.
        """
        xpath = '//em[@class="additional spell phonetic"]'
        try:
            self.phonetic = self.collins_selector.xpath(xpath)[0].text
        except:
            print("Phonetics miss, please check!")
            self.phonetic=""

    def _get_rank(self):
        """
        Get the rank of the word, such as CET-4, CET-6...
        """
        xpath = '//span[@class="via rank"]'
        self.rank = self.collins_selector.xpath(xpath)
        if self.rank:
            self.rank = self.rank[0].text
        else:
            self.rank = ""
            print("The rank of {} is not found, it may be difficult word.".format(self.spelling))

    def _get_explanations(self):
        """
        Get all explanations, including translation, English meaning, example sentences.
        :return: A list containing all collins trans. The structure is :
            [{"property": "U-COUNT",
             "examples_list":,[
                    {"example_EN": "...graduates with degrees in engineering.",
                    "example_CN":  "…获得工程学学位的毕业生。"},]},
            ]
        """

        explanation_xpath = '//div[@class="wt-container"]/ul/li'
        explanation_element_list = self.collins_selector.xpath(explanation_xpath)
        self.trans_list = []
        for explanation_element in explanation_element_list:
            explanation_dict = self._explanation_handle(explanation_element)
            if explanation_dict:
                self.trans_list.append(explanation_dict)

    def _explanation_handle(self, explanation_element):
        """
        :param explanation_element: The xpath is '//div[@class="wt-container"]/ul/li'
        :return:A dict containing the information about the trans. The structure is:
        { "property": "N-UNCOUNT",
        "meaning": 工程;工程学
        "example_list": [ {"example_EN":,"example_CN":}, ]
        }
        """
        property_element = explanation_element.xpath('./div/p/span[@class="additional"]')
        if property_element:
            property = property_element[0].text
        else:
            return None

        meaning = " ".join(explanation_element.xpath('./div/p/text()'))
        meaning = chinese_out(meaning)

        examples_element_list = explanation_element.xpath('./div[@class="exampleLists"]/div')
        examples_list = []
        if examples_element_list:
            for example_element in examples_element_list:
                examples = example_element.xpath('./p')
                example_EN = examples[0].text
                example_CN = examples[1].text
                examples_list.append({"example_EN": example_EN, "example_CN": example_CN})
        return {"property": property, "example_list": examples_list, "meaning": meaning}


def chinese_out(text):
    """
    Select the Chinese character and symbols.
    :param text: The text to be handled
    :return: The Chinese string.
    """
    reg = re.compile(u'[\u4e00-\u9fa5\，\。\；\（\)\;\(\)]')
    res = re.findall(reg, text)
    res = "".join(res)
    return res
