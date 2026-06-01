# tests/test_register_ddt.py
import pytest
import csv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_csv(filename):
    filepath = os.path.join('data', filename)
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

class RegisterPage:
    URL = 'https://demoqa.com/register'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def navigate(self):
        self.driver.get(self.URL)

    def fill_form(self, firstname, lastname, username, password):
        if firstname:
            el = self.wait.until(EC.presence_of_element_located((By.ID, 'firstname')))
            el.clear()
            el.send_keys(firstname)
        if lastname:
            el = self.driver.find_element(By.ID, 'lastname')
            el.clear()
            el.send_keys(lastname)
        if username:
            el = self.driver.find_element(By.ID, 'userName')
            el.clear()
            el.send_keys(username)
        if password:
            el = self.driver.find_element(By.ID, 'password')
            el.clear()
            el.send_keys(password)

    def click_register(self):
        btn = self.wait.until(EC.presence_of_element_located((By.ID, 'register')))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        self.driver.execute_script("arguments[0].click();", btn)

    def is_registered_successfully(self):
        try:
            self.wait.until(EC.url_contains('login'))
            return True
        except:
            return False

class TestRegisterDDT:
    @pytest.mark.parametrize('row', load_csv('register_data.csv'))
    def test_register(self, driver, row):
        page = RegisterPage(driver)
        page.navigate()
        page.fill_form(
            row['firstname'],
            row['lastname'],
            row['username'],
            row['password']
        )
        page.click_register()

        if row['expected'] == 'PASS':
            assert page.is_registered_successfully(), \
                f"[{row['description']}] Registrasi seharusnya BERHASIL"
        else:
            assert not page.is_registered_successfully(), \
                f"[{row['description']}] Registrasi seharusnya GAGAL"