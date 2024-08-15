from django.shortcuts import render, redirect
from .models import *
from .forms import *
from star_ratings.models import UserRating, Rating
from .servicec import *
from django.db.models import Q
from datetime import datetime
import json
from django.http import JsonResponse

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    banners = Banner.objects.all()

    if request.method == 'GET':
        q = request.GET.get('q','').capitalize()
        products = Product.objects.filter(name__icontains=q)

    for product in products:
        try:
            product.rating_average = [i for i in range(int(Rating.objects.get(object_id=product.id).average))]
            product.save()
        except:
            pass

    if request.user.is_authenticated:
        for product in products:
            product.in_cart_status = product.in_cart(request.user)
    else:
        for product in products:
            product.in_cart_status = False

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderitem.quantity = 1
        orderitem.save()
        return redirect('product-list')
    

    context = {
        'products': products,
        'categories': categories,
        'banners':banners,
        'cart_total':cart_total(request),
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    products = Product.objects.all()
    is_liked = False
    comments = Comment.objects.filter(product=product)
    likes = Likes.objects.filter(product=product).count()
    form = CommentForm()
    images = ProductImage.objects.filter(product=product)
    company = product.company
    categories = Category.objects.all()


    for i in comments:
        try:
            i.rating_score = [i for i in range(UserRating.objects.get(user=i.user, rating_id=product.id).score)]
            i.save()
        except:
            i.rating_score = []
        

    if request.user.is_authenticated:
        is_liked = Likes.objects.filter(user=request.user, product=product).exists()
        if request.method == 'POST' and 'like' in request.POST:
            if is_liked:
                Likes.objects.filter(user=request.user, product=product).delete()
            else:
                Likes.objects.create(user=request.user, product=product)
        

    for produkt in products:
        try:
            produkt.rating_average = [i for i in range(int(Rating.objects.get(object_id=product.id).average))]
            produkt.save()
        except:
            pass
    if request.user.is_authenticated:
        product.in_cart_status = product.in_cart(request.user)
    else:
        product.in_cart_status = False


    if request.method == 'POST':
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderitem.quantity = 1
        orderitem.save()
        if 'buy_now' in request.POST:
            return redirect('product-detail', pk=pk)
        elif 'comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                form.instance.product = product
                form.save()
                return redirect('product-detail', pk=pk)
        return redirect('product-detail', pk=pk)

    context = {
        'company': company,
        'produkt':produkt,
        'images':images,
        'product': product,
        'products': products,
        'is_liked': is_liked,
        'likes':likes,
        'form':form,
        'comments':comments,
        'categories': categories,
        'cart_total':cart_total(request),
    }
    return render(request, 'shop/product_detail.html', context)

def company_products(request, pk):
    company = Company.objects.get(id=pk)
    products = Product.objects.filter(company=company)
    categories = Category.objects.all()

    for product in products:
        try:
            product.rating_average = [i for i in range(int(Rating.objects.get(object_id=product.id).average))]
            product.save()
        except:
            pass
    
    context = {
        'company': company,
        'products': products,
        'categories': categories
    }
    return render(request, 'shop/company_products.html', context)


def category_catalog(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()

    if request.user.is_authenticated:
        for product in products:
            product.in_cart_status = product.in_cart(request.user)
    else:
        for product in products:
            product.in_cart_status = False

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderitem.quantity = 1
        orderitem.save()
        return redirect('category-catalog', slug=slug)
    

    context = {
        'products': products,
        'category': category,
        'categories': categories
    }

    return render(request, 'shop/category_catalog.html', context)
def cart_page(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        orders = OrderItem.objects.filter(order=order)
        shipping_adress_exists = ShippingAddress.objects.filter(user=request.user).exists()
        if  shipping_adress_exists:
            shipping_adress = ShippingAddress.objects.get(user=request.user)
        else:
            shipping_adress = None
        order_item_exists = OrderItem.objects.filter(order=order).exists()
        
        if request.method == 'POST':       
            if 'checkout' in request.POST:
                order = Order.objects.get(user=request.user, complete=False)
                orders = OrderItem.objects.filter(order=order)
                if request.method == 'POST':
                    order.complete = True
                    order.save()
                    return redirect('cart-page')
            else:
                orderitem_id = request.POST.get('orderitem_id')
                orderitem = OrderItem.objects.get(id=orderitem_id)
                if 'up' in request.POST:
                    orderitem.quantity += 1
                elif 'down' in request.POST:
                    orderitem.quantity -= 1
                orderitem.save()
                if orderitem.quantity == 0:
                    orderitem.delete() 
    else:
        return redirect('account_login')
        
    context = {
        'order_item_exists':order_item_exists,
        'shipping_adress':shipping_adress,
        'orders': orders,
        'shipping_adress_exists':shipping_adress_exists,
        'cart_total':cart_total(request),
        'order': order
    }
    
    return render(request, 'shop/cart_page.html', context)

def shipping_page(request):

    order = Order.objects.get(user=request.user, complete=False)
    shipping_address_exists = ShippingAddress.objects.filter(user=request.user).exists()
    if shipping_address_exists:
        shipping_address = ShippingAddress.objects.get(user=request.user)
        form =  ShippingAddressForm(instance=shipping_address)
        if request.method == 'POST':
            form = ShippingAddressForm(request.POST, instance=shipping_address)
            if form.is_valid():
                form.instance.user = request.user
                form.instance.order = order
                form.save()
                order.complete = True
                order.save()
                return redirect('cart-page')
    else:    
        form =  ShippingAddressForm()
        if request.method == 'POST':
            form = ShippingAddressForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                form.instance.order = order
                form.save()
                order.complete = True
                order.save()
                return redirect('cart-page')
            
    context = {
        'order': order,
        'form': form,
        'cart_total':cart_total(request),
    }
    return render(request, 'shop/shipping_adress_page.html', context)

def favorites_page(request):
    products = Likes.objects.filter(user=request.user)
    
    context = {
        'products' : products,
        'cart_total':cart_total(request),
    }
    return render (request, 'shop/favorites.html', context)

def pending_page(request):
    order = Order.objects.filter(user=request.user, complete=True)
    orders = OrderItem.objects.filter(Q(status='pending') & Q(order__in=order)).order_by('-id')
    context = {
        'orders': orders,
        'cart_total':cart_total(request),

    }
    return render(request, 'shop/pending.html', context)

def purchases(request):
    order = Order.objects.filter(user=request.user, complete=True)
    my_order = OrderItem.objects.filter(Q(status='delivered') & Q(order__in=order)).order_by('-id')
    context = {
        'my_order': my_order,
        'cart_total':cart_total(request),

    }
    return render(request, 'shop/purchases.html', context)

def process_order(request):
  transaction_id = datetime.now().timestamp()

  if request.user.is_authenticated:
    user = request.user
    order, created = Order.objects.get_or_create(user=user, complete=False)


  order.transaction_id = transaction_id

  order.complete = True
  order.save()


  return JsonResponse('Payment submitted..', safe=False)

def become_seller_page(request):

    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        user.role = 'saller'
        user.save()
        return redirect('/')
    
    context = {
        'cart_total':cart_total(request),

    }
    return render(request, 'shop/become_seller_page.html', context)