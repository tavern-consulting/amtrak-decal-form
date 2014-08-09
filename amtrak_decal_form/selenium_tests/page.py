class UserPanel(object):
    def set_required_fields(self):
        char_fields = [
            ('id_name', 'Name'),
            ('id_location', 'Location'),
            ('id_line1', '123 Foo Dr.'),
            ('id_city', 'Indianapolis'),
            ('id_zip_code', '46260'),
            ('id_phone_number', '317-867-5309'),
            ('id_cost_center', 'Cost Center'),
            ('id_wbs_element', 'WBS Element'),
            ('id_account', 'Account'),
        ]
        for element_id, value in char_fields:
            element = self.driver.find_element_by_id(element_id)
            element.clear()
            element.send_keys(value)

    def validate_and_continue(self):
        continue_link = self.driver.find_element_by_css_selector('a.continue')
        continue_link.click()

    def assert_on_decal_form(self):
        element = self.driver.find_element_by_id('id_rolling_stock_or_not')
        assert element.is_displayed()

    def get_form_errors(self):
        return [
            element.text for element in
            self.driver.find_elements_by_css_selector('.form-errors li')
        ]


class IndexPage(UserPanel):
    def __init__(self, driver):
        self.driver = driver
