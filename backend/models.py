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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.product_name


class Shop(models.Model):
    shop_name = models.CharField(max_length=100, verbose_name="Магазин")
    shop_url = models.URLField(verbose_name="Сайт магазина")
    categories = models.ManyToManyField(Category, through="CategoryShop", related_name="categories")
    products = models.ManyToManyField(Product, through="StockDetailes", related_name="shops")

    def __str__(self):
        return self.shop_name


class StockDetailes(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_detailes",
                                verbose_name="Товар", blank=True)
    shop = models.ForeignKey(Shop, related_name="stock_detailes", on_delete=models.CASCADE, verbose_name="Магазин")
    product_model = models.CharField(max_length=100, verbose_name="Модель")
    stock_level = models.PositiveIntegerField(verbose_name="Количество в наличии")
    stock_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Рекомендованная розничная цена")


class Parameter(models.Model):
    parameter_name = models.CharField(max_length="1000", verbose_name="Параметр")
    product_infos = models.ManyToManyField(StockDetailes, through="ProductParameter", related_name="parameters")





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
    user = models.ForeignKey(User, verbose_name="Пользователь", related_name="orders", on_delete=models.CASCADE)
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=10, verbose_name="Статус заказа")
    order_date = models.DateTimeField(auto_now=True, verbose_name="Дата заказа")
    products = models.ManyToManyField(Product, related_name="orders", verbose_name="Заказы")

    def __str__(self):
        return f"Order status: {self.order_status}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="order_items",
                                verbose_name="Товар в заказе")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products", verbose_name="Заказ")
    order_quantity = models.IntegerField(verbose_name="Количество")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="orders")
