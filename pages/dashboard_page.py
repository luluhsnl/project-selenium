from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    URL = 'https://the-internet.herokuapp.com/secure'

    # ── Locators ──────────────────────────────────────
    LOGOUT_BTN = (By.CSS_SELECTOR, 'a.button.secondary[href="/logout"]')
    FLASH_MSG   = (By.ID, 'flash')

    # ── Actions ───────────────────────────────────────
    def logout(self):
        self.click(self.LOGOUT_BTN)

    # ── Assertion Helpers ─────────────────────────────
    def is_on_dashboard(self):
        return self.get_current_url() == self.URL