import requests
from bs4 import BeautifulSoup
from .cookies import get_cookies
from .models import Shop, Comment
from fake_useragent import UserAgent
import os

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
MEDIA_PATH = os.path.join(BASE_PATH, 'media')


def get_session_with_cookies():
    session = requests.Session()
    session.headers = {'user-agent': UserAgent().random}
    cookies = get_cookies()
    # cookies = [{'domain': 'in-k2web.at', 'expiry': 1684189305, 'httpOnly': False, 'name': 'gate', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '978e14e772731a7e0100f01fdcaa9a80'}, {'domain': 'in-k2web.at', 'httpOnly': False, 'name': 'PHPSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'ne2cur5mtovgpssv1p0aip94es'}, {'domain': 'in-k2web.at', 'expiry': 1684189281, 'httpOnly': False, 'name': 'sfate', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '18d8ac7267406735e262c6bb2b680db5'}]
    print(cookies)

    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    return session


def download_photo(session, photo_url, photo_name):
    s = session.get('https://in-k2web.at/' + photo_url)
    with open(os.path.join(MEDIA_PATH, photo_name), 'wb') as f:
        f.write(s.content)


def count_star(stars):
    with open(os.path.join(os.path.dirname(__file__), 'star.txt')) as f:
        star = f.read()
        return stars.count(star)


def start_parse_comment():
    session = requests.Session()

    shops = Shop.objects.all()

    for shop in shops:
        url = f'https://in-k2web.at/shop/comments/{shop.uuid}'
        page_num = 1
        while True:
            try:
                comment_url = f'{url}/?p={page_num}'
                s = session.get(comment_url)
                bs = BeautifulSoup(s.content, 'html.parser')

                if bs.select('#captcha-img'):
                    session = get_session_with_cookies()
                    continue

                print(comment_url)
                page_num += 1
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

                    photo_name = [i for i in image_url.split('/') if i.endswith('.jpg') or i.endswith('.png')][0]
                    # print(photo_name)
                    download_photo(session, image_url, photo_name)
                    # if image_url != '/img/default_avatar2.jpeg':
                    #     image_url = image_url.split('/')[5]
                    # else:
                    #     image_url = image_url.split('/')[2]
                    check = Comment.objects.filter(content=text)
                    if not check:
                        c = Comment.objects.create(
                            shop=Shop.objects.get(name=shop_name),
                            product=product,
                            nickname=nickname,
                            published=published,
                            content=text,
                            city=city,
                            star_count=star_count - 3,
                            image=photo_name
                        )
                        c.save()
            except Exception as e:
                print(str(e))
