from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from HomeApp.models import Setting, ContactMessage, ContactForm
from ProductApp.models import Product, Images, Category
from django.contrib import messages
from django.urls import reverse
from HomeApp.forms import SearchForm
from OrderApp.models import ShopCart

# Create your views here.


def Home(request):

    current_user = request.user
    cart_product = ShopCart.objects.filter(user_id=current_user.id)
    totalAmount = 0
    productCount = 0
    for pro in cart_product:
        totalAmount += pro.product.new_price * pro.quantity
        productCount += 1

    categories = Category.objects.all()
    settings = Setting.objects.get(id=1)
    sliding_images = Product.objects.all().order_by('id')[:2]
    latest_products = Product.objects.all().order_by('-id')
    products = Product.objects.all()

    context = {
        'categories': categories,
        'settings': settings,
        'sliding_images': sliding_images,
        'latest_products': latest_products,
        'products': products,
        'cart_product': cart_product,
        'totalAmount': totalAmount,
        'productCount': productCount,
    }

    return render(request, 'home.html', context)


def single_product(request, id):
    categories = Category.objects.all()
    settings = Setting.objects.get(id=1)
    single_product = Product.objects.get(id=id)
    images = Images.objects.filter(product_id=id)

    current_user = request.user
    cart_product = ShopCart.objects.filter(user_id=current_user.id)
    totalAmount = 0
    productCount = 0
    for pro in cart_product:
        totalAmount += pro.product.new_price * pro.quantity
        productCount += 1

    # need to filter the related product (need 15 rel product)
    # relatedProducts = Product.objects.all().order_by('id')[:6]
    relatedProducts = Product.objects.raw(
        "SELECT * FROM ProductApp_product WHERE category_id = (SELECT category_id from ProductApp_product WHERE id=%s)", [id])

    context = {
        'categories': categories,
        'settings': settings,
        'single_product': single_product,
        'images': images,
        'relatedProducts': relatedProducts,
        'cart_product': cart_product,
        'totalAmount': totalAmount,
        'productCount': productCount,
    }

    return render(request, 'single_product.html', context)


def category_items(request, id, slug):

    current_user = request.user
    cart_product = ShopCart.objects.filter(user_id=current_user.id)
    totalAmount = 0
    productCount = 0
    for pro in cart_product:
        totalAmount += pro.product.new_price * pro.quantity
        productCount += 1

    sliding_images = Product.objects.all().order_by('id')[:2]
    categories = Category.objects.all()
    settings = Setting.objects.get(id=1)
    cat_items = Product.objects.filter(category_id=id)
    if not cat_items:
        cat_items = Product.objects.raw(
            "SELECT  ProductApp_product.id, ProductApp_product.title,ProductApp_product.brand, ProductApp_product.new_price,ProductApp_product.image FROM ProductApp_category,ProductApp_product where (ProductApp_category.id = ProductApp_product.category_id) AND tree_id = (select tree_id from ProductApp_category WHERE id = %s)", [id])

    context = {
        'sliding_images': sliding_images,
        'categories': categories,
        'settings': settings,
        'cat_items': cat_items,
        'cart_product': cart_product,
        'totalAmount': totalAmount,
        'productCount': productCount,
    }

    return render(request, 'categorical_product.html', context)


def About(request):

    current_user = request.user
    cart_product = ShopCart.objects.filter(user_id=current_user.id)
    totalAmount = 0
    productCount = 0
    for pro in cart_product:
        totalAmount += pro.product.new_price * pro.quantity
        productCount += 1

    categories = Category.objects.all()
    settings = Setting.objects.get(id=1)

    context = {
        'settings': settings,
        'categories': categories,
        'cart_product': cart_product,
        'totalAmount': totalAmount,
        'productCount': productCount,
    }

    return render(request, 'about.html', context)


def Contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # messages.success(request, 'Profile details updated.')

            return HttpResponseRedirect(reverse('contact'))

    form = ContactForm
    categories = Category.objects.all()
    settings = Setting.objects.get(id=1)

    current_user = request.user
    cart_product = ShopCart.objects.filter(user_id=current_user.id)
    totalAmount = 0
    productCount = 0
    for pro in cart_product:
        totalAmount += pro.product.new_price * pro.quantity
        productCount += 1

    context = {
        'form': form,
        'categories': categories,
        'settings': settings,
        'cart_product': cart_product,
        'totalAmount': totalAmount,
        'productCount': productCount,
    }
    return render(request, 'contact_form.html', context)


def SearchView(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            cat_id = form.cleaned_data['cat_id']
            # print(cat_id)
            if cat_id == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(
                    category_id=cat_id, title__icontains=query)

            current_user = request.user
            cart_product = ShopCart.objects.filter(user_id=current_user.id)
            totalAmount = 0
            productCount = 0
            for pro in cart_product:
                totalAmount += pro.product.new_price * pro.quantity
                productCount += 1

            categories = Category.objects.all()
            sliding_images = Product.objects.all().order_by('id')[:2]
            settings = Setting.objects.get(id=1)
            context = {
                'categories': categories,
                'query': query,
                'cat_items': products,
                'sliding_images': sliding_images,
                'settings': settings,
                'cart_product': cart_product,
                'totalAmount': totalAmount,
                'productCount': productCount,
            }
            return render(request, 'categorical_product.html', context)
    return HttpResponseRedirect('category_items')
