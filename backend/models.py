from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=1000, verbose_name="Категория")

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=500, verbose_name="Товар")
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 verbose_name="Категории",
                                 related_name="products")

    def __str__(self):
        return self.product_name


class Shop(models.Model):
    shop_name = models.CharField(max_length=100, verbose_name="Название магазина")
    shop_url = models.URLField(verbose_name="Сайт магазина", blank=True)
    categories = models.ManyToManyField(Category, verbose_name="Категории", related_name="shops")
    products = models.ManyToManyField(Product, through="StockDetailes", verbose_name="Товары", related_name="shops")

    def __str__(self):
        return self.shop_name


class StockDetailes(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар", related_name="stock_detailes")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="Магазин", related_name="stock_detailes")
    product_model = models.CharField(max_length=100, verbose_name="Модель")
    stock_level = models.PositiveIntegerField(verbose_name="Количество в наличии")
    stock_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Рекомендованная розничная цена")

    def __str__(self):
        return f"stock detailes of {self.product_model}"


class Parameter(models.Model):
    parameter_name = models.CharField(max_length="1000", verbose_name="Параметр")
    stock_detailes = models.ManyToManyField(StockDetailes,
                                            through="ParameterPositions",
                                            verbose_name="Сведения об остатках",
                                            related_name="parameters")

    def __str__(self):
        return self.parameter_name


class ParameterPositions(models.Model):
    stock_detailes = models.ForeignKey(StockDetailes,
                                       on_delete=models.CASCADE,
                                       verbose_name="Параметры в наличии",
                                       related_name="parameter_positions")
    parameter = models.ForeignKey(Parameter,
                                  on_delete=models.CASCADE,
                                  verbose_name="Параметр",
                                  related_name="parameter_positions")
    parameter_value = models.CharField(max_length=1000, verbose_name="Значение параметра")

    def __str__(self):
        return  f"parameter value: {self.parameter_value}"


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
    products = models.ManyToManyField(Product, through="OrderItems", verbose_name="Товары", related_name="orders")
    shops = models.ManyToManyField(Shop, through="OrderItems", verbose_name="Магазины", related_name="orders")
    def __str__(self):
        return f"Order: {self.pk} {self.order_status}"


class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар", related_name="order_items")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ", related_name="order_items")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="Магазин", related_name="order_items")
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return f"total quantity ordered: {self.quantity}"


class Contact(models.Model):
    CONTACT_TYPE_CHOICES = (("CNS", "consumer"), ("SPL", "supplier"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="contacts")
    contanct_type = models.CharField(choices=CONTACT_TYPE_CHOICES, verbose_name="Тип контакта")
    phone = models.CharField(max_length=10, verbose_name="Телефон")

    def __str__(self):
        return f"{self.contanct_type} {self.phone}"


class Address(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name="Контакт", related_name="addresses")
    country = models.CharField(max_length=500, verbose_name="Страна")
    zip_code = models.CharField(max_length=10, verbose_name="Почтовый индекс")
    city = models.CharField(max_length=500, verbose_name="Город")
    street = models.CharField(max_length=500, verbose_name="Улица")
    house = models.CharField(max_length=5, verbose_name="Дом")
    building = models.CharField(max_length=3, verbose_name="Строение")
    appart_office = models.CharField(max_length=5, verbose_name="Квартира или офис")

    def __str__(self):
        return f"{self.city} {self.street} {self.house} {self.building} {self.appart_office}"
