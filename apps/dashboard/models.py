from django.db import models
from ..shop.models import Company
# Create your models here.
class Advertisement(models.Model):
    name = models.ForeignKey(Company, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to="images/")


    class Meta:
        verbose_name_plural = "Обьявлении"
