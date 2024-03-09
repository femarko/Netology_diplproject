from django.db import models
from django.contrib.auth.models import User

# todo регистрация пользователей: User Registration Django for APIs Build web APIs with Python and Django
#  William S. Vincent


class Category(models.Model):
    category_name = models.CharField(max_length=1000, verbose_name="Категория")

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=500, verbose_name="Товар")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категории")

    def __str__(self):
        return self.product_name


class Shop(models.Model):
    shop_name = models.CharField(max_length=100, verbose_name="Магазин")
    shop_url = models.URLField(verbose_name="Сайт магазина")
    categories = models.ManyToManyField(Category, verbose_name="Категории", related_name="shops")
    products = models.ManyToManyField(Product, through="StockDetailes", related_name="shops")

    def __str__(self):
        return self.shop_name


class StockDetailes(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name="Товар",
                                related_name="stock_detailes",
                                blank=True)
    shop = models.ForeignKey(Shop,
                             verbose_name="Магазин",
                             on_delete=models.CASCADE,
                             related_name="stock_detailes")
    product_model = models.CharField(max_length=100, verbose_name="Модель")
    stock_level = models.PositiveIntegerField(verbose_name="Количество в наличии")
    stock_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Рекомендованная розничная цена")


class Parameter(models.Model):
    parameter_name = models.CharField(max_length="1000", verbose_name="Параметр")
    stock_detailes = models.ManyToManyField(StockDetailes, through="ParameterValue", related_name="parameters")


class ParameterValue(models.Model):
    stock_detailes = models.ForeignKey(StockDetailes,
                                       on_delete=models.CASCADE,
                                       verbose_name="Параметры в наличии",
                                       related_name="parameter_value")
    parameter = models.ForeignKey(Parameter,
                                  on_delete=models.CASCADE,
                                  verbose_name="Параметр",
                                  related_name="parameter_value")
    parameter_value = models.CharField(max_length=1000, verbose_name="Значение параметра")


class Order(models.Model):

    ORDER_STATUS_CHOICES = (
        ('basket', 'Статус корзины'),
        ('new', 'Новый'),
        ('confirmed', 'Подтвержден'),
        ('assembled', 'Собран'),
        ('sent', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=10, verbose_name="Статус заказа")
    products = models.ManyToManyField(Product, through="OrderItem", verbose_name="Товары", related_name="orders")
    shops = models.ManyToManyField(Shop,
                                   through="OrderItem",
                                   verbose_name="Магазины",
                                   related_name="orders")
    def __str__(self):
        return f"Order status: {self.order_status}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name="Товары",
                                related_name="order_items")
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              verbose_name="Заказ",
                              related_name="order_items")
    shop = models.ForeignKey(Shop,
                             on_delete=models.CASCADE,
                             verbose_name="Магазин",
                             related_name="orders_items")
    quantity = models.PositiveIntegerField(verbose_name="Количество")


class Contact(models.Model):
    CONTACT_TYPE_CHOICES = (("CNS", "consumer"), ("SPL", "supplier"))
    user = models.ForeignKey(User, verbose_name="Пользователь", related_name="contacts", on_delete=models.CASCADE)
    contanct_type = models.CharField(choices=CONTACT_TYPE_CHOICES, verbose_name="Тип контакта")
    phone = models.CharField(max_length=10, verbose_name="Телефон")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.phone


class Address(models.Model):
    contact = models.ForeignKey(Contact,
                                on_delete=models.CASCADE,
                                verbose_name="Контакт пользователя",
                                related_name="addresses")
    country = models.CharField(max_length=500, verbose_name="Страна")
    zip_code = models.CharField(max_length=500, verbose_name="Почтовый индекс")
    city = models.CharField(max_length=500, verbose_name="Город")
    street = models.CharField(max_length=500, verbose_name="Почтовый индекс")
    house = models.CharField(max_length=5, verbose_name="Почтовый индекс")
    building = models.CharField(max_length=3, verbose_name="Почтовый индекс")
    apartement = models.CharField(max_length=5, verbose_name="Почтовый индекс")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f'{self.country} {self.city} {self.street} {self.house}'


class Category(models.Model):
    category_name = models.CharField(max_length=500, verbose_name="Категория товара")
    shops = ''  # todo m2m CategoryShop


