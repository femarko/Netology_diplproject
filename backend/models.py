from django.db import models
from django.contrib.auth.models import User

class CLients:
    """todo регистрация пользователей: User Registration Django for APIs Build web APIs with Python and Django William S. Vincent"""
    pass

class Contact(models.Model):
    CONTACT_TYPE_CHOICES = (("CNS", "consumer"), ("SPL", "supplier"))
    user = models.ForeignKey(User, verbose_name="Пользователь", related_name="contacts", on_delete=models.CASCADE)
    contanct_type = models.CharField(choices=CONTACT_TYPE_CHOICES)
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

#
# class Order(models.Model):
#     ORDER_STATUS_CHOICE = [()]
#     order_status = ''