# pages/checkout_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys


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
        fn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.FIRST_NAME)
        )
        fn.click()
        fn.clear()
        fn.send_keys(first_name)
        fn.send_keys(Keys.TAB)

        ln = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LAST_NAME)
        )
        ln.click()
        ln.clear()
        ln.send_keys(last_name)
        ln.send_keys(Keys.TAB)

        pc = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.POSTAL_CODE)
        )
        pc.click()
        pc.clear()
        pc.send_keys(postal)
        pc.send_keys(Keys.TAB)

    def continue_checkout(self):
        btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.CONTINUE_BTN)
        )
        self.driver.execute_script("arguments[0].click();", btn)
        WebDriverWait(self.driver, 20).until(
            lambda d: 'checkout-step-two' in d.current_url or 'checkout-complete' in d.current_url
        )

    def continue_checkout_expect_error(self):
        btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.CONTINUE_BTN)
        )
        self.driver.execute_script("arguments[0].click();", btn)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.ERROR_MSG)
        )

    def finish_checkout(self):
        btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.FINISH_BTN)
        )
        self.driver.execute_script("arguments[0].click();", btn)
        WebDriverWait(self.driver, 20).until(
            EC.url_contains('checkout-complete')
        )

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
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.ERROR_MSG)
            )
            return True
        except:
            return False

    def get_total(self):
        try:
            el = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.TOTAL_LABEL)
            )
            return el.text
        except:
            return ''