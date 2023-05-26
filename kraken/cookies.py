import time
from twocaptcha import TwoCaptcha
import base64
from selenium.webdriver.common.by import By
# from undetected_chromedriver import Chrome
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

token = '8c7cda1c47a322c23ab33fc3c9bcb0e6'
solver = TwoCaptcha(token, server='rucaptcha.com')
username = 'artokit1dwr'
password = 'AijqlkKmoiInwr51'


def check_start_captcha(driver):
    driver.get('https://in-k2web.at/')
    while True:
        captcha_elem = driver.find_elements(By.CSS_SELECTOR, '#captcha-img')

        if not captcha_elem:
            return

        captcha_elem = captcha_elem[0]

        src = captcha_elem.get_attribute('src')
        photo = base64.b64decode(src.replace('data:image/png;base64,  ', ''))

        with open('cap.png', 'wb') as f:
            f.write(photo)

        res = send_captcha()
        print(f"[{datetime.datetime.now().strftime('%D %T')}] {res}")
        driver.find_element(By.CSS_SELECTOR, '.login-input').send_keys(res)
        driver.find_element(By.CSS_SELECTOR, '.button-submit').click()


def login(driver: Chrome):
    global username, password
    while True:
        captcha_elem = driver.find_elements(By.CSS_SELECTOR, '.captcha img')

        if not captcha_elem:
            return

        captcha_elem = captcha_elem[0]

        username_input, password_input, captcha_input = driver.find_elements(By.CSS_SELECTOR, '.login-input')[:3]

        for elem in (username_input, password_input, captcha_input):
            elem.clear()

        username_input.send_keys(username)
        password_input.send_keys(password)

        src = captcha_elem.get_attribute('src')
        photo = base64.b64decode(src.replace('data:image/jpeg;charset=utf-8;base64, ', ''))

        with open('cap.png', 'wb') as f:
            f.write(photo)

        res = send_captcha()
        captcha_input.send_keys(res)

        driver.find_element(By.CSS_SELECTOR, '.button-submit').click()


def get_cookies():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print(f"[{datetime.datetime.now().strftime('%D %T')}] Браузер запущен")
    check_start_captcha(driver)
    print(f"[{datetime.datetime.now().strftime('%D %T')}] Капча пройдена")
    login(driver)
    time.sleep(10)
    print(f"[{datetime.datetime.now().strftime('%D %T')}] Заебись, парсим")
    cookies = driver.get_cookies()
    driver.close()
    return cookies


def send_captcha():
    while True:
        captcha_text = solver.normal('cap.png').get('code')

        if captcha_text:
            return captcha_text
