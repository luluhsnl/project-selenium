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

    # ── TC-EC-001 ──────────────────────────────────────
    @allure.title('TC-EC-001: Login dengan user valid')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_valid(self, driver):
        with allure.step('Login sebagai standard_user'):
            login = SauceDemoLoginPage(driver)
            login.login(VALID_USER, VALID_PASSWORD)
        with allure.step('Verifikasi redirect ke inventory'):
            assert login.is_login_successful(), 'Login valid harus berhasil'

    # ── TC-EC-002 ──────────────────────────────────────
    @allure.title('TC-EC-002: Login dengan user yang dikunci')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_locked_user(self, driver):
        with allure.step('Login sebagai locked_out_user'):
            login = SauceDemoLoginPage(driver)
            login.login(LOCKED_USER, VALID_PASSWORD)
        with allure.step('Verifikasi muncul pesan error'):
            assert login.is_login_failed(), 'User terkunci harus gagal login'

    # ── TC-EC-003 ──────────────────────────────────────
    @allure.title('TC-EC-003: Login dengan kredensial invalid')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_invalid(self, driver):
        with allure.step('Login dengan username dan password salah'):
            login = SauceDemoLoginPage(driver)
            login.login('wronguser', 'wrongpass')
        with allure.step('Verifikasi muncul pesan error'):
            assert login.is_login_failed(), 'Kredensial invalid harus gagal'

    # ── TC-EC-004 ──────────────────────────────────────
    @allure.title('TC-EC-004: Verifikasi jumlah produk (6 item)')
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_count(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        with allure.step('Verifikasi jumlah produk = 6'):
            inv = InventoryPage(driver)
            assert inv.get_product_count() == 6, 'Harus ada 6 produk'

    # ── TC-EC-005 ──────────────────────────────────────
    @allure.title('TC-EC-005: Urutkan produk harga terendah ke tertinggi')
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_price_low_to_high(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        with allure.step('Sort produk dari harga terendah'):
            inv.sort_by('lohi')
        with allure.step('Verifikasi urutan harga ascending'):
            prices = inv.get_product_prices()
            assert prices == sorted(prices), 'Harga harus urut dari terendah'

    # ── TC-EC-006 ──────────────────────────────────────
    @allure.title('TC-EC-006: Tambah 1 produk ke cart')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_one_to_cart(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        with allure.step('Tambah produk pertama ke cart'):
            inv.add_product_to_cart(0)
        with allure.step('Verifikasi badge cart = 1'):
            assert inv.get_cart_count() == 1, 'Badge cart harus = 1'

    # ── TC-EC-007 ──────────────────────────────────────
    @allure.title('TC-EC-007: Tambah 3 produk, hapus 1, verifikasi badge = 2')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_three_remove_one(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        with allure.step('Tambah 3 produk ke cart'):
            inv.add_product_to_cart(0)
            inv.add_product_to_cart(1)
            inv.add_product_to_cart(2)
        with allure.step('Hapus 1 produk'):
            inv.remove_product_from_cart(0)
        with allure.step('Verifikasi badge cart = 2'):
            assert inv.get_cart_count() == 2, 'Badge cart harus = 2'

    # ── TC-EC-008 ──────────────────────────────────────
    @allure.title('TC-EC-008: Checkout berhasil dengan data lengkap')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_success(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.go_to_cart()
        cart = CartPage(driver)
        cart.click_checkout()
        checkout = CheckoutPage(driver)
        with allure.step('Isi data checkout lengkap'):
            checkout.fill_info('Budi', 'Santoso', '40123')
            checkout.continue_checkout()
            checkout.finish_checkout()
        with allure.step('Verifikasi order terkonfirmasi'):
            assert checkout.is_order_confirmed(), 'Order harus terkonfirmasi'

    # ── TC-EC-009 ──────────────────────────────────────
    @allure.title('TC-EC-009: Checkout gagal - field nama kosong')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_empty_name(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.go_to_cart()
        cart = CartPage(driver)
        cart.click_checkout()
        checkout = CheckoutPage(driver)
        with allure.step('Klik Continue tanpa isi nama'):
            checkout.fill_info('', 'Santoso', '40123')
            checkout.continue_checkout()
        with allure.step('Verifikasi muncul pesan error'):
            assert checkout.has_error(), 'Harus muncul error saat nama kosong'

    # ── TC-EC-010 ──────────────────────────────────────
    @allure.title('TC-EC-010: Verifikasi total harga di confirmation page')
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
        with allure.step('Verifikasi total harga tampil'):
            total = checkout.get_total()
            assert 'Total' in total, 'Total harga harus tampil di halaman konfirmasi'

    # ── TC-EC-011 ──────────────────────────────────────
    @allure.title('TC-EC-011: User dapat logout setelah login')
    @allure.severity(allure.severity_level.NORMAL)
    def test_logout(self, driver):
        login = SauceDemoLoginPage(driver)
        login.login(VALID_USER, VALID_PASSWORD)
        inv = InventoryPage(driver)
        with allure.step('Logout dari aplikasi'):
            inv.logout()
        with allure.step('Verifikasi kembali ke halaman login'):
            assert 'saucedemo.com' in login.get_current_url(), \
                'Harus redirect ke halaman login setelah logout'

    # ── TC-EC-012 ──────────────────────────────────────
    @allure.title('TC-EC-012: Alur penuh Login → Cart → Checkout → Logout')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_full_e2e_flow(self, driver):
        with allure.step('1. Login'):
            login = SauceDemoLoginPage(driver)
            login.login(VALID_USER, VALID_PASSWORD)
            assert login.is_login_successful()

        with allure.step('2. Tambah produk ke cart'):
            inv = InventoryPage(driver)
            inv.add_product_to_cart(0)
            assert inv.get_cart_count() == 1

        with allure.step('3. Checkout'):
            inv.go_to_cart()
            CartPage(driver).click_checkout()
            checkout = CheckoutPage(driver)
            checkout.fill_info('Budi', 'Santoso', '40123')
            checkout.continue_checkout()
            checkout.finish_checkout()
            assert checkout.is_order_confirmed()

        with allure.step('4. Logout'):
            inv2 = InventoryPage(driver)
            driver.get('https://www.saucedemo.com/inventory.html')
            inv2.logout()
            assert 'saucedemo.com' in login.get_current_url()

        allure.attach(
            driver.get_screenshot_as_png(),
            name='e2e_complete',
            attachment_type=allure.attachment_type.PNG
        )
