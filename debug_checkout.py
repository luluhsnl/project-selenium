from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get('https://www.saucedemo.com')

driver.find_element(By.ID, 'user-name').send_keys('standard_user')
driver.find_element(By.ID, 'password').send_keys('secret_sauce')
driver.find_element(By.ID, 'login-button').click()
time.sleep(2)

driver.find_element(By.CSS_SELECTOR, '.btn_inventory').click()
time.sleep(1)
driver.find_element(By.CLASS_NAME, 'shopping_cart_link').click()
time.sleep(1)
driver.find_element(By.ID, 'checkout').click()
time.sleep(1)

fn = driver.find_element(By.ID, 'first-name')
fn.click()
fn.send_keys('Budi')
fn.send_keys(Keys.TAB)

ln = driver.find_element(By.ID, 'last-name')
ln.send_keys('Santoso')
ln.send_keys(Keys.TAB)

pc = driver.find_element(By.ID, 'postal-code')
pc.send_keys('40123')
pc.send_keys(Keys.TAB)

print('URL sebelum:', driver.current_url)
print('First name:', driver.find_element(By.ID, 'first-name').get_attribute('value'))
print('Last name:', driver.find_element(By.ID, 'last-name').get_attribute('value'))
print('Postal:', driver.find_element(By.ID, 'postal-code').get_attribute('value'))

driver.find_element(By.ID, 'continue').click()
time.sleep(2)
print('URL sesudah:', driver.current_url)

time.sleep(3)
driver.quit()
