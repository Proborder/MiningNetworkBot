import time
import random
import pickle
import time
import re
from os import system

from art import tprint
from fake_useragent import UserAgent

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


class MiningNetwork:
    def __init__(self):

        # User-Agent
        useragent = UserAgent()

        # Options
        options = webdriver.ChromeOptions()
        options.add_extension('./extension/1.35.2_10.crx')
        options.add_argument(f'user-agent={useragent.random}')                # Рандомный UserAgent
        options.add_argument('--disable-blink-features=AutomationControlled') # Отключение webdriver
        options.add_argument('--disable-software-rasterizer')                 # Без понятия что
        options.add_argument('start-maximized')                               # Максимальное разрешение
        # options.add_argument('headless') 									  # Фоновый режим

        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=options, service=service)
        self.nft = []


    def clear(self):
        """Clear console"""
        return system('cls')


    def exists_xpath(self, xpath):
        """Check xpath"""
        try:
            self.driver.find_element_by_xpath(xpath)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist


    def closes_driver(self):
        """Closes all driver"""

        self.driver.close()
        self.driver.quit()

        print('[+] Бот закончил работу')


    def sell_shares(self):
        """Sell SHARES"""
        self.driver.get('https://miningnetwork.io/?w=exchange&type=sell')
        time.sleep(10)
        try:
            amount = re.findall(r'\d+', self.driver.find_element_by_xpath("//h3[contains(text(), 'SHARES')]").text)
            self.driver.find_elements_by_xpath("//*[@class='GamePage_inputs_block__3tIEU']/input")[0].clear()
            self.driver.find_elements_by_xpath("//*[@class='GamePage_inputs_block__3tIEU']/input")[0].send_keys(amount)
            time.sleep(2)
            self.driver.find_element_by_class_name('Button_textButton__2ntQv').click()
            print(f'[+] Продал {amount[0]} SHARES')
        except Exception as ex:
            pass


    def collect_id(self, level):
        """Collect all id cards"""
        self.nft.clear()
        id_list = []
        self.driver.get('https://miningnetwork.io/?w=asics')
        time.sleep(3)
        all_id = self.driver.find_elements_by_xpath("//*[@class='BaseWindow_asset_shortcut__xS3Hp']/a")

        for asset in all_id:
            elem_id = re.findall(r'\d+', asset.get_attribute('href'))[0]
            level_elem = self.driver.find_element_by_xpath(f'//a[contains(@href,"{elem_id}")]/../legend').text
            if int(level_elem[5::]) < level:
                self.nft.append(elem_id)

        print(f'[+] Необходимо улучшить {len(self.nft)} асиков')


    def collect_reward(self):
        """Collect all reward"""
        self.driver.get('https://miningnetwork.io/?w=asics')
        time.sleep(2)
        try:
            self.driver.find_element_by_xpath("//*[text()='Collect rewards']").click()
            print('[+] Собрал SHARES')
            time.sleep(10)
        except NoSuchElementException:
            pass


    def upgrade_nft(self):
        """Upgrade nft"""
        for card in self.nft:
            self.driver.get(f'https://miningnetwork.io/?w=asic&id={card}&back=asics')
            time.sleep(5)
            if self.exists_xpath("//*[text()='Upgrade']"):
                self.driver.find_element_by_xpath("//*[text()='Upgrade']").click()
                print(f'[+] Улучшил {card}')
            elif self.exists_xpath("//*[text()='upgrade in progress ']"):
                try:
                    price_up = re.findall(r'\d+', self.driver.find_element_by_xpath("//h5[contains(text(), 'Price: ')]").text)
                    balance = re.findall(r'\d+', self.driver.find_element_by_xpath("//*[@class='GamePage_balance_item__5GOQ4'][3]/div").text)
                    time_up = self.driver.find_element_by_xpath("//p[contains(text(), 'upgrade in progress ')]").text.split(' ')[3][3:5]
                    if int(price_up[0]) < int(balance[0]) / 10 and int(time_up) in range(2, 60 + 1):
                        self.driver.find_element_by_xpath("//*[text()='Speed up']").click()
                        print(f'[+] Ускорил {card}')
                    else:
                        print(f'[+] {card} в процессе улучшения')
                except NoSuchElementException:
                    pass
            elif self.exists_xpath("//*[text()='Insufficient balance']"):
                print(f'[+] {card} не хватает баланса на улучешние')
            elif self.exists_xpath("//*[text()='Stake']"):
                continue

            time.sleep(5)


    def authorization_load(self):
        """Authorization load"""
        self.driver.get("https://wallet.wax.io/dashboard")
        self.clear()
        tprint('Mining Network Bot')
        print('[+] Идёт процесс авторизации...')
        for cookie in pickle.load(open("cookies", "rb")):
            self.driver.add_cookie(cookie)
        self.driver.get("https://miningnetwork.io/?w=asics")
        time.sleep(5)
        self.driver.find_element_by_class_name("Button_textButton__2ntQv").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("div[aria-label='WAX Cloud Wallet']").click()


    def authorization_dump(self):
        """Authorization dump"""
        self.driver.get("https://wallet.wax.io/")
        time.sleep(60)
        pickle.dump(self.driver.get_cookies(), open('cookies', 'wb'))
        self.closes_driver()
