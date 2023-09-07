from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from django.http import JsonResponse
from .forms import CityFormSelect
from .utils import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
import threading
# from .df import *
# from .parser_comments import start_parse_comment
# t = threading.Thread(target=start_parse_comment)
# t.start()
# start_parse_comment()
# from .shop_parser import process
# process()
# thread_shop.start()
# thread_catalog.start()
# thread_comments.start()
# thread_other_page.start()


class Index(LoginRequiredMixin, ListView):
    template_name = 'kraken/index.html'
    model = Shop
    context_object_name = 'shop'
    paginate_by = 20

    def get_queryset(self):
        try:
            user = self.request.user
            user_data = UserData.objects.get(login=user.username)
            city = user_data.city_selected.name.split('(')[0]
            locations = ItemLocation.objects.filter(location__contains=city)
        # print(locations)
            products = Product.objects.filter(locations__in=locations)
            shops = list(set([i.shop for i in products]))
            if self.request.GET.get('q'):
                return [shop for shop in shops if self.request.GET.get('q').lower() in shop.name.lower()]
            # return Shop.objects.filter(name__icontains=self.request.GET.get('q'))
            return shops
        # return Shop.objects.all()
        except:
            return Shop.objects.all()


class NewsList(LoginRequiredMixin, ListView):
    template_name = 'kraken/news.html'
    model = News
    context_object_name = 'news'


class NewsDetail(LoginRequiredMixin, DetailView):
    template_name = 'kraken/news_detail.html'
    model = News

    def get_object(self, queryset=None):
        return News.objects.get(uuid=self.kwargs.get('uuid'))

    def get_context_data(self, **kwargs):
        context = super(NewsDetail, self).get_context_data(**kwargs)
        context['other_news'] = News.objects.exclude(uuid=self.kwargs.get('uuid'))
        return context


class InfoTextView(LoginRequiredMixin, DetailView):
    model = InfoText
    context_object_name = 'text'
    template_name = 'kraken/text.html'
    slug_url_kwarg = 'name'

    def get_context_data(self, **kwargs):
        context = super(InfoTextView, self).get_context_data(**kwargs)
        context['categories'] = InfoCategory.objects.all()
        context['texts'] = InfoText.objects.all()
        context['current_text'] = context['texts'].get(slug=self.kwargs.get('name'))
        return context


class CatalogView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 24
    context_object_name = 'products'
    template_name = 'kraken/catalog.html'
    
    def get_queryset(self):
        try:
            user = self.request.user
            user_data = UserData.objects.get(login=user.username)
            city = user_data.city_selected.name.split('(')[0]
            locations = ItemLocation.objects.filter(location__contains=city)
        # print(locations)
            products = Product.objects.filter(locations__in=locations)
            if self.request.GET.get('q'):
                return products.objects.filter(title__icontains=self.request.GET.get('q'))
            # return Shop.objects.filter(name__icontains=self.request.GET.get('q'))
            return list(set(products))
        # return Shop.objects.all()
        except:
            return Product.objects.all()


class ShopCatalogDetail(LoginRequiredMixin, ShopRateMixin, PagesMixin, DetailView):
    template_name = 'kraken/shop_catalog_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ShopCatalogDetail, self).get_context_data(**kwargs)
        context.update(self.get_pages('Товары'))
        context.update(self.get_rate_context())
        context['products'] = Product.objects.filter(shop=self.shop)
        return context

    def get_object(self, queryset=None):
        self.shop = Shop.objects.get(uuid=self.kwargs.get('uuid'))
        return self.shop


class ShopItem(LoginRequiredMixin, ShopRateMixin, ReviewTopMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'kraken/shop_item.html'

    def get_object(self, queryset=None):
        self.shop = Product.objects.get(uuid=self.kwargs.get('uuid')).shop
        return Product.objects.get(uuid=self.kwargs.get('uuid'))

    def get_context_data(self, **kwargs):
        context = super(ShopItem, self).get_context_data(**kwargs)
        context['locations'] = self.get_locations()
        context.update(self.get_review_context(self.shop.name))
        context['comments'] = Comment.objects.filter(shop=self.shop, product=self.object.title)
        context['summary'] = self.get_summary_rate()
        return context

    def get_locations(self):
        type_order = self.request.GET.get('type')

        if type_order:
            return self.object.locations.filter(buy_type=['ins', 'pre'][type_order == 'pre-order'])

        obj = self.object.locations.filter(buy_type='ins')
        if obj:
            return obj
        else:
            return self.object.locations.filter(buy_type='pre')


class CommentsView(LoginRequiredMixin, ShopRateMixin, ReviewTopMixin, ListView):
    template_name = 'kraken/comments.html'
    context_object_name = 'comments'
    paginate_by = 20

    def get_queryset(self):
        shop = Shop.objects.get(uuid=self.kwargs.get('uuid'))
        self.shop = shop
        return Comment.objects.filter(shop=shop)

    def get_context_data(self, **kwargs):
        context = super(CommentsView, self).get_context_data(**kwargs)
        context['shop_count_all_comments'] = len(Comment.objects.filter(shop=self.shop))
        context.update(self.get_review_context('Отзывы'))
        self.set_rates()
        context.update(self.get_rate_context())
        return context


class VacanciesView(LoginRequiredMixin, ShopRateMixin, PagesMixin, DetailView):
    template_name = 'kraken/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super(VacanciesView, self).get_context_data(**kwargs)
        context.update(self.get_pages('Вакансии'))
        context.update(self.get_rate_context())
        context['products'] = Product.objects.filter(shop=self.shop, type_of_product='Работа')
        return context

    def get_object(self, queryset=None):
        self.shop = Shop.objects.get(uuid=self.kwargs.get('uuid'))
        return self.shop


class OtherPageView(LoginRequiredMixin, ShopRateMixin, ReviewTopMixin, DetailView):
    model = Page
    context_object_name = 'page_info'
    template_name = 'kraken/other_page.html'

    def get_object(self, queryset=None):
        self.shop = Shop.objects.get(uuid=self.kwargs.get('uuid'))
        return Page.objects.get(shop=self.shop, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super(OtherPageView, self).get_context_data(**kwargs)
        context.update(self.get_review_context(self.object.title))
        context.update(self.get_rate_context())
        return context


class AuthView(CaptchaMixin, TemplateView):
    template_name = 'kraken/login.html'

    def get(self, request, *args, **kwargs):
        if not self.request.session.get('start_captcha'):
            return redirect('check')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AuthView, self).get_context_data(**kwargs)
        context.update(self.get_captcha_context(self.request))
        return context


class LoginView(FormView):
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        username = request.POST.get('login')
        password = request.POST.get('password')
        if request.session['captcha_code'] == request.POST.get('captcha').upper():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('index'))
        return redirect('login')


class RegisterView(FormView):
    form_class = UserCreationForm

    def post(self, request, *args, **kwargs):
        if request.session['captcha_code'] == request.POST.get('captcha').upper():
            if request.POST.get('password1') == request.POST.get('password2'):
                username = request.POST.get('login')
                password = request.POST.get('password1')
                first_name = request.POST.get('display_name')
                f = User.objects.create_user(username=username, password=password, first_name=first_name)
                f.save()
                login(request, f)
                UserData(login=username, password=password).save()
                return redirect('select_city')
        return redirect('login')


class ProfileView(LoginRequiredMixin, UserDataMixin, DetailView):
    template_name = 'kraken/profile.html'
    context_object_name = 'user_data'

    def get_object(self, queryset=None):
        return UserData.objects.get(login=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_data'] = self.get_user_data(self.request)
        return context


class SelectCityView(LoginRequiredMixin, FormView):
    template_name = 'kraken/select_city.html'
    context_object_name = 'cities'
    form_class = CityFormSelect

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**ProfileReviewTopMixin.get_user_context(self.request))
        return context


class SelectPostView(LoginRequiredMixin, UpdateView):
    def post(self, request, *args, **kwargs):
        city = City.objects.get(uuid=self.request.POST.get('select_city'))
        user_data = UserData.objects.get(login=request.user.username)
        user_data.city_selected = city
        user_data.save()
        return redirect(reverse('index'))


class FinancesView(LoginRequiredMixin, TemplateView):
    template_name = 'kraken/finances.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**ProfileReviewTopMixin.get_user_context(self.request))
        return context


class OrdersView(LoginRequiredMixin, TemplateView):
    template_name = 'kraken/orders.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**ProfileReviewTopMixin.get_user_context(self.request))
        return context


class NotificationsView(LoginRequiredMixin, TemplateView):
    template_name = 'kraken/notifications.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**ProfileReviewTopMixin.get_user_context(self.request))
        return context


class ProfileSettings(LoginRequiredMixin, UserDataMixin, TemplateView):
    template_name = 'kraken/profile_preferences.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**ProfileReviewTopMixin.get_user_context(self.request))
        context['user_data'] = self.get_user_data(self.request)
        return context


class CouponsView(LoginRequiredMixin, TemplateView):
    template_name = 'kraken/deposit-coupons.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**ProfileReviewTopMixin.get_user_context(self.request))
        return context


@method_decorator(csrf_exempt, name='dispatch')
class ProfileUpdatePhoto(LoginRequiredMixin, UpdateView):
    def post(self, request, *args, **kwargs):
        file = self.request.FILES['avatar']
        user_data = UserData.objects.get(login=self.request.user.username)
        user_data.image = file
        user_data.save()
        return redirect(reverse('preferences'))


@method_decorator(csrf_exempt, name='dispatch')
class ProfilePasswordChange(LoginRequiredMixin, UpdateView):
    def post(self, request, *args, **kwargs):
        user_data = UserData.objects.get(login=self.request.user.username)
        current_password = user_data.password
        data = self.request.POST
        if (data.get('oldpass') == current_password) and (data.get('newpass') == data.get('newpass2')):
            user_data.password = data.get('newpass')
            user_data.save()
            user = self.request.user
            user.set_password(data.get('newpass'))
            user.save()
            login(self.request, user)
        return redirect(reverse('preferences'))


class TicketAdmin(LoginRequiredMixin, TemplateView):
    template_name = 'kraken/create_ticket.html'


class ExchangeOrders(LoginRequiredMixin, TemplateView):
    template_name = 'kraken/exchanges_orders.html'


class ExchangeView(LoginRequiredMixin, ExchangeAmountMixin, ListView):
    template_name = 'kraken/exchange.html'
    model = Exchange
    context_object_name = 'exchanges'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['amount'] = self.get_amount(self.request)
        return context
    
    def get_queryset(self):
        amount = self.get_amount(self.request)
        return Exchange.objects.filter(min_exchange__lte=amount).order_by('?')


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'kraken/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.filter(user=self.request.user)
        return context


class ChatDetail(LoginRequiredMixin, TemplateView):
    template_name = 'kraken/chat_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.filter(user=self.request.user)
        context['shops'] = [i.shop for i in context['tickets']]
        context['user_data'] = UserData.objects.get(login=self.request.user.username)
        context['current_ticket'] = Ticket.objects.get(uuid=kwargs['uuid'])
        context['user_messages'] = context['current_ticket'].messages.filter(user=self.request.user)[::-1]
        return context


class ExchangeDetail(LoginRequiredMixin, ExchangeAmountMixin, DetailView):
    model = Exchange
    template_name = 'kraken/exchange_detail.html'
    context_object_name = 'exchange'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['amount'] = self.get_amount(self.request)
        return context

    def get_object(self, queryset=None):
        return Exchange.objects.get(uuid=self.kwargs.get('uuid'))


class ExchangeCreateView(LoginRequiredMixin, ExchangeAmountMixin, CreateView):
    template_name = 'kraken/index.html'
    model = ExchangeInfo

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        amount = self.get_amount(self.request)
        exchange = Exchange.objects.get(uuid=kwargs.get('uuid'))
        word = '-'.join([generate_word(4) for _ in range(4)])
        e = ExchangeInfo(amount=amount, exchange=exchange, random_number=word)
        e.save()
        return redirect(e)


class ExchangeInfoView(LoginRequiredMixin, ExchangeAmountMixin, DetailView):
    template_name = 'kraken/exchangeinfo_detail.html'
    model = ExchangeInfo
    context_object_name = 'order'

    def get_object(self, queryset=None):
        order = ExchangeInfo.objects.get(uuid=self.kwargs.get('order'))
        return order

    def get_context_data(self, **kwargs):
        context = super(ExchangeInfoView, self).get_context_data()
        context['exchange'] = Exchange.objects.get(uuid=self.kwargs.get('exchange'))
        return context


class CreateTicketShop(LoginRequiredMixin, FormView):
    template_name = 'kraken/shop_ticket.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        shop = Shop.objects.get(uuid=kwargs['slug'])
        t = Ticket(user=self.request.user, shop=shop, title=request.POST['title'])
        t.save()
        m = Message(user=self.request.user, text=request.POST['message'])
        m.save()
        t.messages.add(m)
        t.save()
        return redirect('/chat')


class CaptchaStart(TemplateView):
    template_name = 'kraken/captcha_start.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = Captcha.objects.order_by('?')[0]
        self.request.session['captcha_code'] = obj.code
        context['captcha'] = obj
        return context


def check_captcha(request):
    code = request.POST['answer'].upper()
    if code == request.session['captcha_code'].upper():
        request.session['start_captcha'] = True
        return redirect('login')
    return redirect('check')


def jquery_get(request):
    return JsonResponse({'code': 1})


def logout_request(request):
    logout(request)
    return redirect(reverse('login'))


def create_message(request, ticket_uuid):
    ticket = Ticket.objects.get(uuid=ticket_uuid)
    m = Message(user=request.user, text=request.POST['message'])
    m.save()
    ticket.messages.add(m)
    ticket.save()
    return redirect('/chat')
