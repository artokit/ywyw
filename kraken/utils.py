from .models import *
import random


class ShopRateMixin:
    shop: Shop = None
    rates = None

    def set_rates(self):
        d = Comment.objects.filter(shop=self.shop)
        s = {
            5: len(d.filter(star_count=5)),
            4: len(d.filter(star_count=4)),
            3: len(d.filter(star_count=3)),
            2: len(d.filter(star_count=2)),
            1: len(d.filter(star_count=1)),
        }
        self.rates = s

    def get_summary_rate(self):
        self.set_rates()
        summ = (self.rates[1] + self.rates[2] + self.rates[3] + self.rates[4] + self.rates[5])
        if summ == 0:
            return 0
        return round(
            (self.rates[1] + self.rates[2] * 2 + self.rates[3] * 3 + self.rates[4] * 4 + self.rates[5] * 5) / summ,
            1
        )

    def get_rate_context(self):
        self.set_rates()
        return {
            'rates': self.rates,
            'summary': self.get_summary_rate()
        }


class PagesMixin:
    shop: Shop = None

    def get_pages(self, title):
        pages = {}
        DEFAULT_SHOP_PAGES = {
            'Товары': f'/shop/catalog/{self.shop.uuid}/',
            'Отзывы': f'/shop/comments/{self.shop.uuid}/',
            'Вакансии': f'/shop/vacancies/{self.shop.uuid}/',
        }
        pages.update(DEFAULT_SHOP_PAGES)
        pages.update({i.title: f'/shop/page/{self.shop.uuid}/{i.slug}/' for i in self.shop.other_pages.all()})
        return {'pages': pages, 'current_page': title}


class ReviewTopMixin(PagesMixin):
    shop = None

    def get_review_context(self, title):
        return {
            'shop': self.shop,
            **self.get_pages(title)
        }


class CaptchaMixin:
    @staticmethod
    def get_captcha_context(request):
        captcha = Captcha.objects.order_by('?')[0]
        request.session['captcha_code'] = captcha.code
        return {'captcha': captcha}


class ProfileReviewTopMixin:
    @staticmethod
    def get_user_context(request):
        return {'user_data': UserData.objects.get(login=request.user.username)}


class UserDataMixin:
    @staticmethod
    def get_user_data(request):
        return UserData.objects.get(login=request.user.username)


class ExchangeAmountMixin:
    @staticmethod
    def get_amount(request):
        try:
            return round(float(request.GET.get('amount', 2500)))
        except:
            return 2500


def generate_word(c):
    s = ''
    letters = 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    for _ in range(c):
        s += random.choice(letters)
    return s

