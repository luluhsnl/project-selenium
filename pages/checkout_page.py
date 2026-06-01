
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time

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
        btn = self.driver.find_element(*self.CONTINUE_BTN)
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(3)

    def finish_checkout(self):
        btn = self.driver.find_element(*self.FINISH_BTN)
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(3)

    def is_order_confirmed(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.url_contains('checkout-complete')
            )
            return True
        except:
            return False

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)

    def has_error(self):
        return self.is_visible(self.ERROR_MSG)

    def get_total(self):
        try:
            el = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.TOTAL_LABEL)
            )
            return el.text
        except:
            return ''