from django.shortcuts import render, redirect
from ..shop.models import *
from .forms import *
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def product_list(request):
    products = Product.objects.all()


    context = {
        'products': products
    }
    return render(request, 'dashboard/product_list.html', context)

def category_list(request):

    category = Category.objects.all()
        
    context = {
        'category': category
    }

    return render(request, 'dashboard/category_list.html', context)

def company_list(request):
    companies = Company.objects.all()

    context = {
        'companies': companies,
    }

    return render(request, 'dashboard/company_list.html', context)

def edit_p(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
        return redirect('d-product-list')


    context = {
        'product': product,
        'form': form
    }
    return render(request, 'dashboard/edit_product.html', context)

def company_detail(request, company_id):
    company = Company.objects.get(id=company_id)
    products = Product.objects.filter(company=company)

    context = {
        'products':products
    }

    return render(request, 'dashboard/company_deteil.html', context)

def order_list(request):

    order_items = OrderItem.objects.filter(product__company__user=request.user).order_by('-id')

    context = {
        'order_items': order_items
    }

    return render(request, 'dashboard/order_list.html', context)

def add_product(request):

    form = AddProductForm()
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('d-product-list')
        

    context = {
        'form': form
    }

    return render(request, 'dashboard/add_product.html', context)

def edit_status(request, pk):
    order = OrderItem.objects.get(id=pk)
    form = EditStatusForm(instance=order)
    if request.method == 'POST':
        form = EditStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
        return redirect('d-order-list')

    context = {
        'order': order,
        'form': form
    }

    return render(request, 'dashboard/edit_status.html', context)

def submit_an_ad(request):

    form = AdvertisementForm()

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('dashboard')
    
    context = {
        'form': form
    }

    return render(request, 'dashboard/submit_an_ad.html', context)