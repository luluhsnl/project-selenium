# pages/inventory_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class InventoryPage(BasePage):
    URL = 'https://www.saucedemo.com/inventory.html'

    SORT_DROPDOWN    = (By.CLASS_NAME, 'product_sort_container')
    PRODUCT_NAMES    = (By.CLASS_NAME, 'inventory_item_name')
    PRODUCT_PRICES   = (By.CLASS_NAME, 'inventory_item_price')
    ADD_TO_CART_BTNS = (By.CSS_SELECTOR, '[data-test^=add-to-cart]')
    REMOVE_BTNS      = (By.CSS_SELECTOR, '[data-test^=remove]')
    CART_BADGE       = (By.CLASS_NAME, 'shopping_cart_badge')
    CART_ICON        = (By.CLASS_NAME, 'shopping_cart_link')
    BURGER_MENU      = (By.ID, 'react-burger-menu-btn')
    LOGOUT_LINK      = (By.ID, 'logout_sidebar_link')

    def sort_by(self, option):
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(option)

    def add_product_to_cart(self, index=0):
        btns = self.driver.find_elements(*self.ADD_TO_CART_BTNS)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btns[index])
        self.driver.execute_script("arguments[0].click();", btns[index])

    def remove_product_from_cart(self, index=0):
        btns = self.driver.find_elements(*self.REMOVE_BTNS)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btns[index])
        self.driver.execute_script("arguments[0].click();", btns[index])

    def go_to_cart(self):
        btn = self.find(self.CART_ICON)
        self.driver.execute_script("arguments[0].click();", btn)

    def logout(self):
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)

    def get_product_count(self):
        return len(self.driver.find_elements(*self.PRODUCT_NAMES))

    def get_cart_count(self):
        try:
            return int(self.get_text(self.CART_BADGE))
        except:
            return 0

    def get_product_prices(self):
        els = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [float(el.text.replace('$', '')) for el in els]

    def is_on_inventory(self):
        return 'inventory' in self.get_current_url()