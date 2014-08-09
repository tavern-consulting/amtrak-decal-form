from django.test import LiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver

from amtrak_decal_form.selenium_tests.page import IndexPage


class UserPanelTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver()
        super(UserPanelTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(UserPanelTestCase, cls).tearDownClass()

    def test_form_is_filled_out_correctly(self):
        self.driver.get(self.live_server_url)
        index_page = IndexPage(self.driver)

        index_page.set_required_fields()
        index_page.validate_and_continue()
        index_page.assert_on_decal_form()

    def test_form_is_not_filled_out_correctly(self):
        self.driver.get(self.live_server_url)
        index_page = IndexPage(self.driver)

        index_page.validate_and_continue()
        with self.assertRaises(AssertionError):
            index_page.assert_on_decal_form()
