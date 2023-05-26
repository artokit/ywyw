import subprocess
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


class Parser:
    def __init__(self):
        self.login = 'artokit1dwr'
        self.password = 'AijqlkKmoiInwr51'
        self.URI = 'https://in-k2web.at/'
        self.driver = uc.Chrome()
        self.driver.maximize_window()
        self.auth()
        print(self.driver.get_cookies())

    def auth(self):
        global ADMIN_ID
        self.driver.get(self.URI)
        while self.driver.find_elements(By.ID, 'captcha-img'):
            captcha = self.driver.find_element(By.ID, 'captcha-img')
            captcha.screenshot('cap.jpg')
            f = open('cap.txt', 'w')
            f.close()
            subprocess.Popen('python tg_bot.py')
            cap = self.get_captcha()
            self.driver.find_element(By.CSS_SELECTOR, '.login-input').send_keys(cap.upper())
            self.driver.find_element(By.CLASS_NAME, 'button-submit').click()
            time.sleep(10)

        while self.driver.find_elements(By.CLASS_NAME, 'captcha'):
            inputs = self.driver.find_elements(By.CLASS_NAME, 'login-input')[:3]
            inputs[0].send_keys(self.login)
            inputs[1].send_keys(self.password)
            captcha = self.driver.find_element(By.CLASS_NAME, 'captcha img')
            captcha.screenshot('cap.jpg')
            f = open('cap.txt', 'w')
            f.close()
            subprocess.Popen('python tg_bot.py')
            cap = self.get_captcha()
            inputs[2].send_keys(cap)
            self.driver.find_element(By.CLASS_NAME, 'button-submit').click()
            time.sleep(10)

    @staticmethod
    def get_captcha():
        while True:
            f = open('cap.txt')
            cap = f.read()
            f.close()
            if cap:
                return cap
            time.sleep(.3)
