from django import template
from django.template.defaultfilters import floatformat

from ..models import UserData, InfoCategory, InfoText, Exchange
PRICE_1_BTC = 1648251
register = template.Library()


@register.simple_tag()
def convert_btc_to_rub(rub_price):
    return round(rub_price / PRICE_1_BTC, 8)


@register.simple_tag()
def float_to_int(price):
    return int(price)


@register.simple_tag()
def progress_bar_for_rate(rate, length):
    if length == 0:
        return 0
    return round(rate/length*100, 1)


@register.simple_tag()
def formatted_float(value, arg=2):
    value = floatformat(value, arg=arg)
    return str(value).replace(',', '.')


@register.inclusion_tag('custom_tags/draw_star.html', takes_context=False)
def draw_stars(star_count):
    return {
        'star_count': star_count
    }


@register.simple_tag()
def get_user_image(user):
    return UserData.objects.get(login=user.username).image


@register.simple_tag()
def get_categories():
    return InfoCategory.objects.all()[:3]


@register.inclusion_tag('custom_tags/draw_text.html')
def get_texts_by_category(cat):
    return {
        'texts': InfoText.objects.filter(category=cat)
    }


@register.simple_tag()
def get_amount_with_commission(obj: Exchange, amount: int):
    return round(amount*(1+obj.commission/100), 2)


@register.simple_tag()
def get_btc_amount(obj: Exchange, amount: int):
    c = get_amount_with_commission(obj, amount)
    return round(c/obj.exchange_rate, 8)

