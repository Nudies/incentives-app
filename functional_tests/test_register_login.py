import unittest
from selenium.webdriver.common.keys import Keys
from base import FunctionalTest


class NewUserTest(FunctionalTest):

    def test_cannot_login_without_register(self):
        # User points browser to homepage
        self.browser.get(self.server_url)

        # Notices title and header
        self.assertIn('Virtual Incentives', self.browser.title)
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Decipher Incentives', header)

        # User accidently tries to login before registering
        inputbox = self.find_element('email', 'id')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Email address'
        )

        # Enters an email
        inputbox.send_keys('User@decipherinc.com')
        # Enters a random password
        inputbox = self.find_element('password', 'id')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Password'
        )
        inputbox.send_keys('hunter2')
        # Tries to login
        self.find_element('login', 'id').send_keys(Keys.ENTER)
        # Notices they are still on the login page
        # and an error message appeared
        self.assertRegexpMatches(self.browser.current_url, '/login/')

        # User realizes they need to register
        # They hit register link
        self.find_element('Register', 'link').send_keys(Keys.ENTER)
        self.assertRegexpMatches(self.browser.current_url, '/register/')

        # Fills out register form and enters home page
        self.find_element('name', 'id').send_keys('User')
        self.find_element('email', 'id').send_keys('User@decipherinc.com')
        self.find_element('password', 'id').send_keys('hunter2')
        self.find_element('confirm', 'id').send_keys('hunter2')
        ## Shit, how do I get around captcha...
        ## Recaptcha always is 'valid' when TESTING=True
        self.find_element('register', 'id').send_keys(Keys.ENTER)
        # User is now at the home page
        self.assertRegexpMatches(self.browser.current_url, self.server_url)
        greeting = self.find_elements('h4', 'tag')
        ## TODO: Need to set up a test db now or we will always error
        self.assertIn('Welcome to Decipher Incentive Requests!',
                      [txt for ele.text in greeting])


if __name__ == '__main__':
    unittest.main()
