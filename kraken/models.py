import random
from django.contrib.auth.models import User
from django.db import models
import uuid


def generate_random_id():
    return random.randint(0, 999999999999999999)


class Page(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=50)
    content = models.TextField()


class Shop(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=150)
    photo = models.ImageField()
    big_photo = models.ImageField(null=True)
    deals_count = models.CharField(max_length=100, default='0')
    other_pages = models.ManyToManyField(Page)

    def __str__(self):
        return self.name

    def get_rate(self):
        d = Comment.objects.filter(shop=self)
        s = {
            5: len(d.filter(star_count=5)),
            4: len(d.filter(star_count=4)),
            3: len(d.filter(star_count=3)),
            2: len(d.filter(star_count=2)),
            1: len(d.filter(star_count=1)),
        }
        summ = (s[1] + s[2] + s[3] + s[4] + s[5])
        if summ == 0:
            return 0
        return round(
            (s[1] + s[2] * 2 + s[3] * 3 + s[4] * 4 + s[5] * 5) / summ,
            1
        )


class News(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=150)
    content = models.TextField()
    preview_text = models.TextField(null=True)
    date = models.DateField()

    def __str__(self):
        return self.name


class InfoCategory(models.Model):
    name_of_category = models.CharField(max_length=50)

    def __str__(self):
        return self.name_of_category


class InfoText(models.Model):
    slug = models.SlugField(primary_key=True)
    title = models.CharField(max_length=150)
    category = models.ForeignKey(InfoCategory, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.title


class ProductPhoto(models.Model):
    photo = models.ImageField()


class ItemLocation(models.Model):
    TYPES = (('ins', 'Моментальный'), ('pre', 'Предзаказ'))
    buy_type = models.CharField(choices=TYPES, max_length=3)
    location = models.CharField(max_length=150)
    location_more_info = models.CharField(max_length=150, blank=True, null=True)
    location_type = models.CharField(max_length=150, blank=True, null=True)
    count = models.CharField(max_length=30)
    rub_price = models.FloatField()

    def __str__(self):
        return f'{self.location} | {self.count} | {self.rub_price}'


class Product(models.Model):
    uuid = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=130)
    type_of_product = models.CharField(max_length=150)
    description = models.TextField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    photos = models.ManyToManyField(ProductPhoto, editable=False)
    locations = models.ManyToManyField(ItemLocation, editable=False)

    def get_price(self):
        try:
            location = self.locations.order_by('rub_price')[0]
            return [location.count, location.rub_price]
        except IndexError:
            return [0, 0]

    def get_rate(self):
        d = Comment.objects.filter(product=self.title)
        s = {
            5: len(d.filter(star_count=5)),
            4: len(d.filter(star_count=4)),
            3: len(d.filter(star_count=3)),
            2: len(d.filter(star_count=2)),
            1: len(d.filter(star_count=1)),
        }
        summ = (s[1] + s[2] + s[3] + s[4] + s[5])
        if summ == 0:
            return 0
        return round(
            (s[1] + s[2] * 2 + s[3] * 3 + s[4] * 4 + s[5] * 5) / summ,
            1
        )

    def __str__(self):
        return self.title


class Comment(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, db_constraint=False)
    product = models.TextField()
    nickname = models.CharField(max_length=150)
    published = models.CharField(max_length=150)
    content = models.TextField()
    city = models.CharField(max_length=150)
    star_count = models.IntegerField()
    image = models.ImageField(default='default_avatar2.jpeg')

    def __str__(self):
        return f'{self.nickname} {self.published}'


class Captcha(models.Model):
    image = models.ImageField()
    code = models.CharField(max_length=15)

    def __str__(self):
        return self.code


class City(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Exchange(models.Model):
    uuid = models.UUIDField(null=True)
    name = models.CharField(max_length=150)
    image = models.ImageField(default='default_avatar2.jpeg')
    exchange_rate = models.FloatField()
    count = models.FloatField()
    min_exchange = models.FloatField()
    commission = models.FloatField()
    card = models.CharField(max_length=150, null=True)
    
    def __str__(self):
        return self.name


class UserData(models.Model):
    login = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    image = models.ImageField(default='default_avatar2.jpeg')
    city_selected = models.ForeignKey(City, on_delete=models.CASCADE, default='11f5916f-5293-443a-9fbf-faa7f36069e7')

    def __str__(self):
        return self.login


class ExchangeInfo(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    random_number = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()

    def get_absolute_url(self):
        return f'/exchange/{self.exchange.uuid}/order/{self.uuid}'

    def __str__(self):
        return self.random_number


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(null=True, blank=True)
    data = models.DateTimeField(auto_now=True, auto_created=True)


class Ticket(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    title = models.TextField(verbose_name='Тема')
    # content = models.TextField(verbose_name='Содержание тикета')
    date = models.DateTimeField(auto_now=True, auto_created=True)
    messages = models.ManyToManyField(Message)

    def __str__(self):
        return f"{self.shop.name} - {self.title}"
