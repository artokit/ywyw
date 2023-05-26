import time

from selenium.webdriver.common.by import By
# from .models import Shop
from parser import Parser
import os


def process():
    p = Parser()
    page_num = 1
    while page_num <= 110:
        print('Страница номер', page_num)
        p.driver.get(f'{p.URI}?p={page_num}')
        page_num += 1
        urls = [elem.get_attribute('href') for elem in p.driver.find_elements(By.CSS_SELECTOR, '.shop-card-item a')]
        for url in urls:
            # try:
            # breakpoint()
            p.driver.get(url)
            uuid = url.replace('https://in-k2web.at/shop/catalog/', '').replace('/', '')
            name = p.driver.find_element(By.CLASS_NAME, 'shop_title').text.strip()
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')
            # file_name =
            # TODO: Парсер фоток
            elem_photo = p.driver.find_element(By.CSS_SELECTOR, '.shop_panel_img img')
            photo_name = elem_photo.get_attribute('src').split('/')[-1].replace('/', '')
            elem_photo.screenshot(os.path.join(path, photo_name))

            elem_photo = p.driver.find_element(By.CSS_SELECTOR, '.shop_top_img img')
            p.driver.execute_script("document.querySelector('.shop_panel').remove()")
            time.sleep(.5)
            photo_big_name = elem_photo.get_attribute('src').split('/')[-1].replace('/', '')
            elem_photo.screenshot(os.path.join(path, photo_big_name))

            count_deals = p.driver.find_element(By.CSS_SELECTOR, '.shop_rait_text span').text.strip()
            print(
                uuid,
                name,
                photo_name,
                photo_big_name,
                count_deals,
            )
            # download_photo(photo_url, photo_name)
            # g = driver.get(f'https://in-k2web.at/shop/catalog/{u}/')
            # print(f'https://in-k2web.at/shop/catalog/{u}/')
            # print(photo_url)
            # print(u)
            # print(name)
            # print()
            # card_items.append(CardItem(photo_url, name, u))
            # count_deals, big_photo = get_last_info(g)
            # s = Shop(uuid=u, name=name, photo=photo_name, big_photo=big_photo, deals_count=count_deals)
            # s.save()
        # except Exception as e:
        #     print(str(e))


process()
