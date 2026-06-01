import pytest
from pages.dashboard_page import DashboardPage

class TestLogin:
    def test_login_valid(self, login_page):
        login_page.login('tomsmith', 'SuperSecretPassword!')
        assert login_page.is_login_successful(), 'Login valid harus berhasil'

    def test_login_invalid_password(self, login_page):
        login_page.login('tomsmith', 'wrongpassword')
        assert login_page.is_login_failed(), 'Login dengan password salah harus gagal'

    def test_login_empty_username(self, login_page):
        login_page.login('', 'SuperSecretPassword!')
        assert login_page.is_login_failed(), 'Login tanpa username harus gagal'

    def test_flash_message_content(self, login_page):
        login_page.login('wronguser', 'wrongpass')
        msg = login_page.get_flash_message()
        assert 'invalid' in msg.lower(), f'Pesan error tidak sesuai: {msg}'

    def test_logout_after_login(self, login_page, driver):
        # 1: Login dulu
        login_page.login('tomsmith', 'SuperSecretPassword!')
        assert login_page.is_login_successful(), 'Login harus berhasil dulu'

        # 2: Pastiin ada di dashboard
        dashboard = DashboardPage(driver)
        assert dashboard.is_on_dashboard(), 'Harus ada di dashboard sebelum logout'

        # 3: Logout dan verifikasi kembali ke halaman login
        dashboard.logout()
        assert 'login' in login_page.get_current_url(), \
            'Setelah logout harus redirect ke halaman login'