import pytest
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

@pytest.fixture(scope='function')
def driver():
    """Fixture: buat driver baru setiap test, tutup setelah selesai"""
    options = webdriver.EdgeOptions()
    options.add_argument('--start-maximized')
    if os.getenv('CI'):
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

    d = webdriver.Edge(
        service=Service(EdgeChromiumDriverManager().install()),
        options=options
    )
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
            print(f'\nScreenshot disimpan: {name}.png')