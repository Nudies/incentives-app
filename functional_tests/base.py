import sys
import unittest

from selenium import webdriver


class FunctionalTest(unittest.TestCase):
    # TODO: Setup a test database and destroy
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
            cls.server_url = 'http://localhost:5000'

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def find_element(self, key, type):
        if type == 'tag':
            return self.browser.find_element_by_tag_name(key)
        elif type == 'id':
            return self.browser.find_element_by_id(key)
        elif type == 'link':
            return self.browser.find_element_by_link_text(key)
        else:
            raise KeyError('%s is not a valid search param' % type)

    def find_elements(self, key, type):
        if type == 'tag':
            return self.browser.find_elements_by_tag_name(key)
        elif type == 'class':
            return self.browser.find_elements_by_class_name(key)
        else:
            raise KeyError('%s is not a valid search param' % type)
