'''
Simple chrome browser htl, javascript parser

v0.1 jul 2019
hdaniel@ualg.pt
'''
from hdlib.net.ChromeBrowser import ChromeBrowser

##############
# Unit tests #
##############
import unittest
from typing import ClassVar, List

class TestChromeBrowser(unittest.TestCase):
    """Unit tests"""

    browser      : ClassVar[ChromeBrowser]
    linkResponse : ClassVar[List[str]]

    @classmethod
    def setUpClass(cls) -> None:
        #code to be executed only once before all tests start
        cls.browser = ChromeBrowser()   #(hideBrowser=False)
        cls.linkResponse = ['C00 https://www.dropbox.com/sh/yyiyfphdfokmoue/AABjE4myhqrT0MzqEDRPGspGa/temp/C00?dl=0',
                            'C15 https://www.dropbox.com/sh/yyiyfphdfokmoue/AACleIDyB83Ho2xFwmu9d8aFa/temp/C15?dl=0',
                            'C35 https://www.dropbox.com/sh/yyiyfphdfokmoue/AAA8kBgtxIZ1z1g8YChkFPqZa/temp/C35?dl=0',
                            'element "C44" NOT found']


    def setUp(self):
        #code to be executed before each test
        url = 'https://www.dropbox.com/sh/yyiyfphdfokmoue/AADqfkTgo6Pa9BUgntidAXs0a/temp'
        TestChromeBrowser.browser.getPage(url)


    def testgetElementByLinkText0(self) -> None:
        '''find existing elements'''
        linkText = ['C00', 'C15', 'C35', 'C44']
        for l,s in zip(linkText, TestChromeBrowser.linkResponse):
            element = TestChromeBrowser.browser.getElementByLinkText(l)
            if element is not None:
                strtext = "{} {}".format(l, element.get_attribute('href'))
            else:
                strtext = 'element "{}" NOT found'.format(l)
            print(strtext)
            self.assertEqual(strtext, s)


if __name__ == "__main__":       
	try:
		unittest.main()
	#avoid exception inside vscode when exiting unittest
	except SystemExit as e: 
		pass