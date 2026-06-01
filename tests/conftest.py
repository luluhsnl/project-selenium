# tests/conftest.py
import pytest
import os
from selenium import webdriver

@pytest.fixture(scope='function')
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    d = webdriver.Chrome(options=options)
    yield d
    d.quit()

@pytest.fixture(scope='function')
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            os.makedirs('reports/screenshots', exist_ok=True)
            name = item.nodeid.replace('/', '_').replace('::', '_')
            driver.save_screenshot(f'reports/screenshots/{name}.png')