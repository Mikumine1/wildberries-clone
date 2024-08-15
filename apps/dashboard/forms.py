from django import forms
from ..shop.models import *
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'price', 'company', 'category', 'status']

        widgets = {
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class' : 'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'price':forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
            'company':forms.Select(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'})
        }

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'price', 'company', 'category', 'status']

        widgets = {
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'Название'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Описание'}),
            'price':forms.TextInput(attrs={'class':'form-control', 'type':'number', 'placeholder':'Цена'}),
            'company':forms.Select(attrs={'class':'form-control', 'col':'10'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'})
        }

class EditStatusForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['status']

        widgets = {
            'status':forms.Select(attrs={'class':'form-control'})
        }

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['name', 'image']

        widgets = {
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'name':forms.Select(attrs={'class' : 'form-control', 'placeholder':'Название'}),
        }