# pages/cart_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    # ── Locators ──────────────────────────────────────
    CART_ITEMS    = (By.CLASS_NAME, 'cart_item')
    CHECKOUT_BTN  = (By.ID, 'checkout')
    CONTINUE_BTN  = (By.ID, 'continue-shopping')

    # ── Actions ───────────────────────────────────────
    def click_checkout(self):
        self.click(self.CHECKOUT_BTN)

    def continue_shopping(self):
        self.click(self.CONTINUE_BTN)

    # ── Assertion Helpers ─────────────────────────────
    def get_item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def is_on_cart(self):
        return 'cart' in self.get_current_url()