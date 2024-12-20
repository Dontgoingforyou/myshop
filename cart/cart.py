from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon

class Cart:
    def __init__(self, request):
        """ Инициализация корзины """

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранение пустой корзины в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Сохранение примененного купона
        self.coupon_id = self.session.get('coupon_id')

    def __iter__(self):
        """ Прокрутка товара в корзине в цикле и получение товаров из БД """

        product_ids = self.cart.keys()
        # Получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """ Подсчет всех товаров в корзине """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """ Добавление товара в корзину, либо обновление его количества """

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """ Пометка сеанса как "измененный", чтобы обеспечить его сохранение """
        self.session.modified = True

    def remove(self, product):
        """ Удаление товара из корзины """

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """ Расчет общей стоймости товаров в корзине """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """ Удаление корзины из сеанса """

        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        """ Метод определяется как свойство. Если корзина содержит coupon_id, то возвращается объект Coupon с id """

        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """ Если в корзине есть купон, извлекается его скидка и высчитывается сумма,
            которая будет вычтена из общей суммы корзины """

        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        """ Метод возвращает сумму корзины """
        return self.get_total_price() - self.get_discount()