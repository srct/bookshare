# functional tests describe a 'user story', testing how the implementation works
# with a complete black box as to how it works on the backend

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from django.contrib.auth.models import User
from core.models import Student
from trades.models import Listing


# your mason username and password are neccessary to log in for test cases
username = 'gmason'
password = 'Gunston_Ha11'

def sign_in_user(self):
    """ Hits the proper buttons to log a student in through Mason CAS."""

    # He lands on the the front page, and decide to log in.
    self.browser.find_element_by_link_text('Log In').click()

    # He is redirected login.gmu.edu, where he sees the username and
    # password fields.
    self.assertIn('Mason Central Authentication Service', self.browser.title)
    username_input = self.browser.find_element_by_id('username')
    password_input = self.browser.find_element_by_id('password')

    # He types in his username and password...
    username_input.send_keys(username)
    password_input.send_keys(password)

    # ...and hits the submit button.
    self.browser.find_element_by_class_name('btn-submit').click()

    # George is then redirected back to the homepage.
    self.assertIn(u'SRCT Bookshare \u2022 Homepage', self.browser.title)

def sign_out_user(self):
    """ Hits the proper buttons to log a student out through Mason CAS."""

    # George is on a nonadmin page with SRCT Bookshare, and wants to log out.
    self.browser.find_element_by_link_text('Log Out').click()

    # He is redirected to login.gmu.edu...
    self.assertIn('Mason Central Authentication Service', self.browser.title)

    # and sees a successful logout message.
    self.assertIn(u'Logout successful', self.browser.find_element_by_tag_name('h2').text)

class SeleniumSetUpTearDown(StaticLiveServerTestCase):
    """TestCase subclass to add Selenium setup and teardown."""

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        pass
        # self.browser.quit()


class FirstTimeLogIn(SeleniumSetUpTearDown):
    """Tests that a Student is created and all their attributes set on a user's
       initial login."""

    def setUp(self):
        # in the database
        # other Student
        # good Listing (other Student)
        # bad Listing (other Student)
        # George's other Listing
        return super(FirstTimeLogIn, self).setUp()

    def tearDown(self):
        return super(FirstTimeLogIn, self).tearDown()

    def not_test_student_creation(self):
        # George Mason lands on Bookshare for the first time, and decides to
        # log in.

        # sign_in_user()

        # He lands on the homepage (not an error page!)

        # He then clicks on his gravatar icon in the navbar...

        # ...and is redirected to his user page.

        # His full name and email are displayed on his user page.

        # George has to run, so he hits the log out button, but he's excited
        # to return later.        
        # sign_out_user()
        pass

class ListingTests(SeleniumSetUpTearDown):
    """Tests all the user interactions pertaining to the models in the trades app."""

    def setUp(self):
        # other Student
        # good Listing (other Student)
        # bad Listing (other Student)
        # George's other Listing
        return super(ListingTests, self).setUp()

    def tearDown(self):
        return super(ListingTests, self).tearDown()

    def test_listing_management(self):
        # George Mason has previously used Bookshare, but wants to sign in and
        # create a new Listing.
        self.browser.get(self.live_server_url)
        self.assertIn(u'SRCT Bookshare \u2022 Homepage', self.browser.title)

        sign_in_user(self)

        # He clicks on 'Create Listing' button in the navbar to add his new
        # textbook.
        self.browser.find_element_by_link_text('Create Listing').click()

        # He his sent to the Create Listing page, where he sees a number of
        # fields to post his Listing.
        self.assertIn(u'SRCT Bookshare \u2022 Create Listing', self.browser.title)
        isbn_input = self.browser.find_element_by_id('id_isbn')
        course_abbr_input = self.browser.find_element_by_id('id_course_abbr')
        condition_input = Select(self.browser.find_element_by_id('id_condition'))
        access_code_input = Select(self.browser.find_element_by_id('id_access_code'))
        price_input = self.browser.find_element_by_id('id_price')
        # TODO: uploading a photo
        description_input = self.browser.find_element_by_id('id_description')

        # He types in his ISBN...
        isbn_input.send_keys('0807830534')
        # ...and is pleasantly surprised to see the title and more autocompleted.

        # TODO: test javascript

        # He then fills out his post's remaining fields.
        course_abbr_input.send_keys('HIST 121')

        condition_input.select_by_value(u'Like New')
        access_code_input.select_by_value(u'Access Code NOT Included')

        price_input.send_keys('20')
        description_input.send_keys('I would be willing to trade this book for one that I need next semester.')

        # George has gotten to the bottom of the page and clicks on Submit...
        self.browser.find_element_by_id('submit-id-submit').click()

        # ...where he is redirected to his new listing's page.
        self.assertIn(u'SRCT Bookshare \u2022 George Mason : Forgotten Founder',
                      self.browser.title)

        # George thinks he may have acted in haste, so decides to cancel his
        # Listing. He sees the 'Cancel Listing' button and clicks it.
        self.browser.find_element_by_link_text('Cancel Listing').click()

        # George then sees the confirmation page...
        self.assertIn(u'SRCT Bookshare \u2022 George Mason : Forgotten Founder \u2022 Cancel',
                      self.browser.title)
        
        # and elects follow through with the cancellation.
        self.browser.find_element_by_xpath("//input[@value='Cancel Your Listing']").click()

        # He is then redirected back to his listing page, and now there's a
        # large danger alert saying the listing has been cancelled.
        self.assertIn(u'SRCT Bookshare \u2022 George Mason : Forgotten Founder',
                      self.browser.title)
        self.assertIn(u'This listing has been cancelled.',
                      self.browser.find_element_by_class_name('alert-danger').text)

        # George however is indecisive, and decides he in fact does want the
        # the listing open for others to bid on it. He clicks on the 'Reopen
        # Listing' button...
        self.browser.find_element_by_link_text('Reopen Listing').click()

        # ...and is sent to a confirmation page to reopen his Listing.
        self.assertIn(u'SRCT Bookshare \u2022 George Mason : Forgotten Founder \u2022 Reopen',
                      self.browser.title)

        # He clicks to confirm he wants his listing back open...
        self.browser.find_element_by_xpath("//input[@value='Reopen Your Listing']").click()

        # ...and is sent back to the Listing's page, this time sans any alerts
        self.assertIn(u'SRCT Bookshare \u2022 George Mason : Forgotten Founder',
                      self.browser.title)
        with self.assertRaises(NoSuchElementException):
            self.assertIn(u'This listing has been cancelled.',
                          self.browser.find_element_by_class_name('alert-danger').text)

        # George thinks he's offering his textbook for a little too low of a
        # price, so decides to edit his Listing to increase the price. He clicks
        # on the 'Edit Listing' button...
        self.browser.find_element_by_link_text('Edit Listing').click()

        # ...where he's sent to a Listing editing page.
        self.assertIn(u'SRCT Bookshare \u2022 George Mason : Forgotten Founder \u2022 Edit',
                      self.browser.title)

        # He sees the fields on the page and finds the one for price.
        price_input = self.browser.find_element_by_id('id_price')

        # George increases his asking price for the textbook.
        price_input.clear()
        price_input.send_keys('30')

        # He then hits Submit...
        self.browser.find_element_by_xpath("//input[@value='Update']").click()
        
        # and is sent back to the Listing page...
        self.assertIn(u'SRCT Bookshare \u2022 George Mason : Forgotten Founder',
                      self.browser.title)
       
        # and his asking price has also been updated.
        self.assertIn(u'$30', self.browser.find_element_by_class_name('price').text)

        # George is finished up for now, so he hits the log out button on the navbar.
        sign_out_user(self)

    def not_test_bidding(self):
        # self.browser.get('http://localhost:8000')

        # sign_in_user()

        # George finds himself on someone else's listing page.

        # George drives a hard bargain

        # sign_out_user()

        pass

    def not_test_flagging(self):

        # self.browser.get('http://localhost:8000')

        # sign_in_user()

        # sign_out_user()

        pass

    def not_test_exchanging(self):

       # self.browser.get('http://localhost:8000')

       # sign_in_user()

       # sign_out_user()

        pass

    def not_test_rating(self):

       # self.browser.get('http://localhost:8000')

       # sign_in_user()

       # sign_out_user()

        pass

class LookoutTests(SeleniumSetUpTearDown):
    """Tests all the user interactions pertaining to the models in the lookouts app."""

    def setUp(self):
        # make sure that a Julius Caesar Lookout doesn't already exist
        return super(LookoutTests, self).setUp()

    def tearDown(self):
        # delete the George Mason Lookout
        return super(LookoutTests, self).tearDown()

    def test_lookout_management(self):
        # George Mason wishes to create a lookout for a book for his class.
        self.browser.get(self.live_server_url)
        self.assertIn(u'SRCT Bookshare \u2022 Homepage', self.browser.title)

        sign_in_user(self)

        # George decides to create a lookout by clicking the Create button
        # on the front page.
        self.browser.find_element_by_link_text('Create').click()

        # He is sent to the Lookout creation page...
        self.assertIn(u'SRCT Bookshare \u2022 Create Lookout', self.browser.title)

        # and then sees the ISBN field.
        isbn_input = self.browser.find_element_by_id('id_isbn')

        # He types in the ISBN of a textbook he'd like to automatically
        # search for...
        isbn_input.send_keys('0743482743')

        # ...and then hits submit.
        self.browser.find_element_by_id('submit-id-submit').click()

        # He is then redirected to the lookout detail page, where he can see a
        # lookout has been created, and all the listings to choose from.
        self.assertIn(u'SRCT Bookshare \u2022 Lookouts \u2022 The Tragedy Of Julius Caesar',
                      self.browser.title)

        # George however decides that he doesn't actually need a lookout for
        # this ISBN, and clicks the delete button.
        self.browser.find_element_by_link_text('Delete this Lookout').click()

        # He's redirected to a confirmation page. George clicks 'delete'.
        self.assertIn(u'SRCT Bookshare \u2022 Delete Lookout',
                      self.browser.title)
        self.browser.find_element_by_xpath("//input[@value='Confirm']").click()

        # George gets redirected back the the homepage.
        self.assertIn(u'SRCT Bookshare \u2022 Homepage', self.browser.title)

        # Finished, he hits the log out button in the navbar.
        sign_out_user(self)
