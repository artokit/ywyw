import dataclasses
# import re
import threading
import requests
# from selenium import webdriver
# import undetected_chromedriver as uc
# from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import sqlite3
import os
from .models import *
# import undetected_chromedriver as uc
# from fake_useragent import UserAgent
from .cookies import get_cookies

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_PATH, 'db.sqlite3')
MEDIA_PATH = os.path.join(BASE_PATH, 'media')
connect = sqlite3.connect(DB_PATH)
cursor = connect.cursor()
URI = 'https://in-k2web.at/'


def set_cookies():
    cookies = get_cookies()
    # cookies = [{'domain': 'in-k2web.at', 'expiry': 1683591652, 'httpOnly': False, 'name': 'gate', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '13e7982896aa99afad1afcdf2ec6dc0a'}, {'domain': 'in-k2web.at', 'httpOnly': False, 'name': 'PHPSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '6c2cu7rujq96rso2efucvspbbm'}, {'domain': 'in-k2web.at', 'expiry': 1683591642, 'httpOnly': False, 'name': 'sfate', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '9a2c7731101425da71b0f95d3322ad9f'}]
    print(cookies)
    for i in cookies:
        session.cookies.set(i['name'], i['value'])
    # for i in cookies:
    #     driver.add_cookie(i)


def download_photo(photo_url, photo_name):
    s = session.get(URI + photo_url)
    with open(os.path.join(MEDIA_PATH, photo_name), 'wb') as f:
        f.write(s.content)


@dataclasses.dataclass
class CardItem:
    image_url: str
    name: str
    uuid: str


def get_urls(content):
    bs = BeautifulSoup(content, 'html.parser')
    for elem in bs.select('.shop-card-item'):
        try:
            photo_url = elem.select_one('img').get('src')
            u = elem.select_one('a').get('href').split('/')[3]
            name = elem.select_one('.shop-card-item-title').text.strip()
            photo_name = photo_url.split('/')[5]
            download_photo(photo_url, photo_name)
            g = session.get(f'https://in-k2web.at/shop/catalog/{u}/')
            f = open('data.txt', 'a')
            print(f'https://in-k2web.at/shop/catalog/{u}/', file=f)
            print(photo_url, file=f)
            print(u, file=f)
            print(name, file=f)
            print('', file=f)
            f.close()
            # card_items.append(CardItem(photo_url, name, u))
            count_deals, big_photo = get_last_info(g)
            s = Shop(uuid=u, name=name, photo=photo_name, big_photo=big_photo, deals_count=count_deals)
            s.save()
        except Exception as e:
            print(str(e))


def get_last_info(response):
    content = response.content
    bs = BeautifulSoup(content, 'html.parser')
    count_deals = int(bs.select_one('.shop_rait_text span').text)
    big_photo = bs.select_one('.shop_top_img img').get('src')
    photo_name = big_photo.split('/')[5]
    download_photo(big_photo, photo_name)
    return count_deals, photo_name


def get_comments():
    for shop in Shop.objects.all():
        page_num = 1
        while True:
            try:
                s = session.get(f'https://in-k2web.at/shop/comments/{shop.uuid}/?p={page_num}')
                print(f'https://in-k2web.at/shop/comments/{shop.uuid}/?p={page_num}')
                page_num += 1
                content = s.content
                bs = BeautifulSoup(content, 'html.parser')
                comments = bs.select('.review_comments_item')

                if not comments:
                    break

                for comment in comments:
                    if 'admin_comment' in comment.get('class'):
                        continue
                    prod = comment.select('.review_comments_title span')[0].text.strip()
                    nickname = comment.select('.review_comments_title')[0].text.replace(prod, '').strip()
                    published = comment.select('.review_comments_data')[0].text.strip()
                    text = comment.select('.review_comments_text')[0].text.strip()
                    try:
                        city = comment.select('.city')[0].text.strip()
                    except IndexError:
                        city = ''
                    stars_content = comment.select('.review_comments_star')[0].prettify()
                    star_count = count_star(stars_content)
                    shop_name = bs.select_one('.shop_title').text.strip()
                    product = comment.select_one('.review_comments_title span').text.strip()
                    image_url = comment.select('img')[0].get('src')
                    if image_url != '/img/default_avatar2.jpeg':
                        download_photo(image_url, image_url.split('/')[5])
                        image_url = image_url.split('/')[5]
                    else:
                        image_url = image_url.split('/')[2]
                    c = Comment.objects.create(
                        shop=Shop.objects.get(name=shop_name),
                        product=product,
                        nickname=nickname,
                        published=published,
                        content=text,
                        city=city,
                        star_count=star_count-3,
                        image=image_url
                    )
                    c.save()
            except Exception as e:
                print(str(e))


def get_catalog_urls(content):
    bs = BeautifulSoup(content, 'html.parser')
    urls = bs.select('.category_product_wrap a')
    for elem in urls:
        try:
            url = elem.get('href')
            u = url.split('/')[3]
            f = open('data.txt', 'a')
            print(f'https://in-k2web.at/shop/item/{u}/', file=f)
            f.close()
            title, type_of_product, content, shop, photos = get_info_item(f'https://in-k2web.at/shop/item/{u}/')
            p = Product(
                uuid=u,
                title=title,
                type_of_product=type_of_product,
                description=content,
                shop=shop
            )
            p.save()
            for i in photos:
                p.photos.add(i)
            p.save()
            s1 = session.get(f'https://in-k2web.at/shop/item/{u}/?type=pre-order')
            s2 = session.get(f'https://in-k2web.at/shop/item/{u}/?type=instant')
            p1 = parse_item_locations(s1.content, 'pre')
            p2 = parse_item_locations(s2.content, 'ins')
            for i in p1:
                p.locations.add(i)
            p.save()
            for i in p2:
                p.locations.add(i)
            p.save()
        except Exception as e:
            print('Error:', str(e))


def get_info_item(url):
    r = session.get(url)
    bs = BeautifulSoup(r.content, 'html.parser')
    title = bs.select_one('.slider_info_title').text.strip()
    type_of_product = bs.select_one('.slider_info_type').text.strip()
    content = bs.select_one('.slider_info_text').prettify()
    shop_uuid = bs.select_one('.breadcrumbs a').get('href').split('/')[3]
    shop = Shop.objects.get(uuid=shop_uuid)
    photos = []
    for photo in bs.select('.item_slider_left label img'):
        photo_name = photo.get('src').split('/')[5]
        download_photo(photo.get('src'), photo_name)
        p = ProductPhoto(photo=photo_name)
        p.save()
        photos.append(p)
    return title, type_of_product, content, shop, photos


def count_star(stars):
    with open(os.path.join(os.path.dirname(__file__), 'star.txt')) as f:
        star = f.read()
        return stars.count(star)


def parse_item_locations(content, type_of_order):
    bs = BeautifulSoup(content, 'html.parser')
    item_locations = []
    for elem in bs.select('.item_location_box'):
        location = elem.select_one('.location_box_text').text.strip()
        more_location = elem.select_one('.location_box_city')
        if more_location:
            more_location = more_location.text.strip()
        else:
            more_location = ''

        location_type = elem.select_one('.location_type_text')
        if location_type:
            location_type = location_type.text.strip()
        else:
            location_type = ''
        count = elem.select_one('.location_size_text').text.strip()
        rub_price = float(elem.select_one('.location_btn_box a').text.replace('руб.', ''))
        il = ItemLocation(
            buy_type=type_of_order,
            location=location,
            location_more_info=more_location,
            location_type=location_type,
            count=count,
            rub_price=rub_price
        )
        il.save()
        item_locations.append(il)
    return item_locations


# driver = uc.Chrome()
# driver.get(URI)
session = requests.Session()
# session.headers = session1.headers
# session = cfscrape.create_scraper(sess=session1)
# session.proxies = {
#     'http': 'http://5e9d97d6-548853:uw6d7ghilf@109.236.80.193:21408',
#     'https': 'http://5e9d97d6-548853:uw6d7ghilf@109.236.80.193:21408',
# }
# input('Авторизуйтесь')
set_cookies()
# driver.quit()


def parse_catalog():
    page_num = 168
    max_page_num = 400
    while page_num <= max_page_num:
        f = open('data.txt', 'a')
        print('Страница номер', page_num, file=f)
        f.close()
        r = session.get(f'https://in-k2web.at/catalog/?p={page_num}')
        get_catalog_urls(r.content)
        page_num += 1


def parse_other_page():
    shops = Shop.objects.all()
    counter = 1
    for shop in shops:
        try:
            other_pages = []
            print(counter, len(shops), f'https://in-k2web.at/shop/catalog/{shop.uuid}/')
            counter += 1
            s = session.get(f'https://in-k2web.at/shop/catalog/{shop.uuid}/')
            bs = BeautifulSoup(s.content, 'html.parser')
            urls = [elem for elem in bs.select('.shop_nav_box a') if '/page/' in elem.get('href')]
            for elem in urls:
                title = elem.text.strip()
                print(title)
                path = elem.get('href')
                print('https://in-k2web.at' + path)
                s = session.get('https://in-k2web.at' + path)
                bs = BeautifulSoup(s.content, 'html.parser')
                content = bs.select_one('.about_wrap').prettify()
                p = Page(
                    # slug=path.split('/')[4],
                    title=title,
                    content=content
                )
                p.save()
                other_pages.append(p)

            for page in other_pages:
                shop.other_pages.add(page)
                shop.save()
        except Exception as e:
            print(str(e))


def parse_shop():
    page_num = 1
    while page_num <= 110:
        r = session.get(f'https://in-k2web.at/?p={page_num}')
        page_num += 1
        get_urls(r.content)
        f = open('data.txt', 'a')
        print('Страница номер', page_num, file=f)
        f.close()


thread_shop = threading.Thread(target=parse_shop)
thread_catalog = threading.Thread(target=parse_catalog)
thread_comments = threading.Thread(target=get_comments)
thread_other_page = threading.Thread(target=parse_other_page)
