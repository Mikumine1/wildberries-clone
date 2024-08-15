from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    ROLE = (
        ('admin', 'Администратор'),
        ('customer', 'Заказчик'),
        ('seller', 'Продавец'),
    )
    role = models.CharField(max_length=100, null=True, blank=True, choices=ROLE)