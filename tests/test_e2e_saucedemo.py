# tests/test_e2e_saucedemo.py
import allure
import pytest
from pages.saucedemo_login_page import SauceDemoLoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

VALID_USER     = 'standard_user'
LOCKED_USER    = 'locked_out_user'
VALID_PASSWORD = 'secret_sauce'

@allure.feature('E-Commerce SauceDemo')
class TestSauceDemo:

    @allure.title('TC-EC-001: Login dengan user valid')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_valid(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        assert login.is_login_successful()

    @allure.title('TC-EC-002: Login dengan user yang dikunci')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_locked_user(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(LOCKED_USER, VALID_PASSWORD)
        assert login.is_login_failed()

    @allure.title('TC-EC-003: Login dengan kredensial invalid')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_invalid(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login('wronguser', 'wrongpass')
        assert login.is_login_failed()

    @allure.title('TC-EC-004: Verifikasi jumlah produk 6 item')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_count(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        assert inv.get_product_count() == 6

    @allure.title('TC-EC-005: Sort produk harga terendah ke tertinggi')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_sort_price_low_to_high(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        inv.sort_by('lohi')
        prices = inv.get_product_prices()
        assert prices == sorted(prices)

    @allure.title('TC-EC-006: Tambah 1 produk ke cart')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_one_to_cart(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        assert inv.get_cart_count() == 1

    @allure.title('TC-EC-007: Tambah 3 hapus 1 badge = 2')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_three_remove_one(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.add_product_to_cart(1)
        inv.add_product_to_cart(2)
        inv.remove_product_from_cart(0)
        assert inv.get_cart_count() == 2

    @allure.title('TC-EC-008: Checkout berhasil')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_success(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.go_to_cart()
        CartPage(driver).click_checkout()
        checkout = CheckoutPage(driver)
        checkout.fill_info('Budi', 'Santoso', '40123')
        checkout.continue_checkout()
        checkout.finish_checkout()
        assert checkout.is_order_confirmed()

    @allure.title('TC-EC-009: Checkout gagal nama kosong')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_empty_name(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.go_to_cart()
        CartPage(driver).click_checkout()
        checkout = CheckoutPage(driver)
        checkout.fill_info('', 'Santoso', '40123')
        checkout.continue_checkout()
        assert checkout.has_error()

    @allure.title('TC-EC-010: Verifikasi total harga')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_total_price_on_confirmation(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.go_to_cart()
        CartPage(driver).click_checkout()
        checkout = CheckoutPage(driver)
        checkout.fill_info('Budi', 'Santoso', '40123')
        checkout.continue_checkout()
        total = checkout.get_total()
        assert 'Total' in total

    @allure.title('TC-EC-011: Logout setelah login')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logout(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        inv.logout()
        assert 'saucedemo.com' in login.get_current_url()

    @allure.title('TC-EC-012: Full E2E flow')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_full_e2e_flow(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        assert login.is_login_successful()

        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        assert inv.get_cart_count() == 1

        inv.go_to_cart()
        CartPage(driver).click_checkout()
        checkout = CheckoutPage(driver)
        checkout.fill_info('Budi', 'Santoso', '40123')
        checkout.continue_checkout()
        checkout.finish_checkout()
        assert checkout.is_order_confirmed()

        driver.get('https://www.saucedemo.com/inventory.html')
        InventoryPage(driver).logout()
        assert 'saucedemo.com' in login.get_current_url()