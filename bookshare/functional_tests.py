# functional tests

#import mechanize
import unittest
from selenium import webdriver


class SeleniumSetUpTearDown(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()


class BookshareNotLoggedInTest(SeleniumSetUpTearDown):

    def test_static_pages_load(self):
        # George Mason is going to Bookshare for the first time and wants to
        # see what it's all about. He tries to go to each of the pages he
        # can visit without logging in.

        self.browser.get('http://localhost:8000')

        heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(heading.text, 'Current Polls')

        self.browser.find_element_by_link_text('How awesome is TDD?').click()

        self.assertIn(u'SRCT Bookshare \u2022 Homepage', self.browser.title)

        self.browser.get('http://localhost:8000/about')

        self.assertIn(u'SRCT Bookshare \u2022 About', self.browser.title)

        self.browser.get('http://localhost:8000/privacy')

        self.assertIn(u'SRCT Bookshare \u2022 Privacy', self.browser.title)

class BookshareLoggedInActionTest(SeleniumSetUpTearDown):

    def test_new_user(self):
        pass

    def test_returing_user(self):
        pass

    def test_post_a_listing(self):
        # George is on the Bookshare homepage, and decides he wants to post
        # a listing. He clicks the 'Create Listing' button in the navbar.

        # He is taken to Create Listing page.

        # He sees a form to post his Listing.

        # He creates a listing for his biography, 'George Mason, Forgotten Founder'.

        # He clicks 'Create'.

        # He is redirected to a page with the details of his listing.
        pass

    def test_edit_a_listing(self):
        pass

    def test_cancel_a_listing(self):
        # George is on his listing page, and decides to cancel his listing. He
        # clicks on the 'Cancel Listing' button in the middle of the page.

        # He is taken to a confirmation page.

        # He clicks that yes, he does want to cancel his listing.

        # He is redirected back to his listing page, but this time with a
        # 'This listing has been cancelled' danger banner across the top.
        pass

    def reopen_a_listing(self):
        # George decides perhaps he didn't want to cancel his listing after all.
        # He clicks on the 'Reopen Listing' button in the middle of the page.

        # He is taken to a confirmation page.

        # He clicks that yes, he does want to reopen his listing.

        # He is redirected back to his listing page, which now no longer has
        # the cancellation danger banner across the top.
        pass


    def test_flag_a_listing(self):
        pass

    def test_remove_a_flag(self):
        pass

    def test_create_a_bid(self):
        pass

    def test_edit_a_bid(self):
        pass

    def test_exchange_a_listing(self):
        pass

    def test_cancel_an_exchange(self):
        pass

    def test_rate_an_exchange(self):
        pass

    def test_edit_a_rating(self):
        pass

    def test_delete_a_rating(self):
        pass

    def test_create_a_lookout(self):
        pass

    def test_delete_a_lookout(self):
        pass

    def test_search_for_a_listing(self):
        pass

# class BookshareLoggedInPassiveTest(SeleniumSetUpTearDown):

# visit recent listings
# visit charts
# visit a lookout page
# visit your profile page
# visit another user's profile page
# your profile ratings
# visit another's profile ratings

# cas_url = 'https://login.gmu.edu/login'
# br = mechanize.Browser()
# br.set_handle_robots(False)
# br.open(cas_url)
# print br.open(cas_url)
# br.select_form(nr=0)
# br['username'] = 'dbond2'
# br['password'] = 'chG4b6a33n'
# br.method = "POST"
# response = br.submit()

if __name__ == '__main__':
    unittest.main()
