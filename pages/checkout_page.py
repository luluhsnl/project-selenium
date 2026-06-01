# pages/checkout_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    FIRST_NAME   = (By.ID, 'first-name')
    LAST_NAME    = (By.ID, 'last-name')
    POSTAL_CODE  = (By.ID, 'postal-code')
    CONTINUE_BTN = (By.ID, 'continue')
    FINISH_BTN   = (By.ID, 'finish')
    SUCCESS_MSG  = (By.CLASS_NAME, 'complete-header')
    ERROR_MSG    = (By.CSS_SELECTOR, '[data-test=error]')
    TOTAL_LABEL  = (By.CLASS_NAME, 'summary_total_label')

    def fill_info(self, first_name, last_name, postal):
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal)

    def continue_checkout(self):
        btn = self.find_clickable(self.CONTINUE_BTN)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        self.driver.execute_script("arguments[0].click();", btn)

    def finish_checkout(self):
        btn = self.find_clickable(self.FINISH_BTN)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        self.driver.execute_script("arguments[0].click();", btn)

    def is_order_confirmed(self):
        return self.is_visible(self.SUCCESS_MSG)

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)

    def has_error(self):
        return self.is_visible(self.ERROR_MSG)

    def get_total(self):
        return self.get_text(self.TOTAL_LABEL)