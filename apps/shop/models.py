from django.db import models
from apps.user.models import User
from django.core.files import File
import io
from PIL import Image as PilImage


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.TextField(null=True, max_length=100)
    slug = models.SlugField(max_length=100, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, null=True, blank=True)
    logo = models.ImageField(upload_to="logo/", null=True, blank=True)

    def last_product(self):
        return self.product_set.all().last()
  
    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name



class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return self.product.name 
         
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    image = models.ImageField(upload_to="images/")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    STATUS = (
        ('schebuled', 'Заплонирован'),
        ('publish', 'Публичный'),
        ('inactive', 'Неактивный'),
    )
    status = models.CharField(max_length=20, choices=STATUS, default='inactive')


    def in_cart(self, user):
        order = Order.objects.filter(user=user, complete=False)
        if order.exists():
            order = order[0]
            if order.orderitem_set.filter(product=self).exists():
                return True
            else:
                return False
        else:
            return False


    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
    
    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        return sum([item.quantity for item in orderitems])
    
    def get_cart_total_amount(self):
        orderitems = self.orderitem_set.all()
        return sum([item.quantity * item.product.price for item in orderitems])
    
    def __str__(self):
        return self.user.username
    
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    date_time = models.DateTimeField(auto_now_add=True)

    STATUS = (
        ('pending', 'В ожидании'),
        ('delivered', 'Доставлен'),
    )
    status = models.CharField(max_length=20, choices=STATUS, default='pending')

    @property
    def get_total(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказов"

    def __str__(self):
        return self.product.name

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        return self.address

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return f"{self.user} - {self.product}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
       return f"{self.user} - {self.text}"


class Banner(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="banner/")

    class Meta:
        verbose_name = "Рeкламный баннер"
        verbose_name_plural = "Рeкламные баннеры"

    def __str__(self):
       return f"{self.company}"


