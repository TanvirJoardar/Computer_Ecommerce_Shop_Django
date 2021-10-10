from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, reverse
from ProductApp.models import Category, Product, Images
from OrderApp.models import ShopCart, ShopingCartForm, Order, OderForm, OderProduct
from HomeApp.models import Setting
from django.contrib import messages
from UserApp.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string


# Create your views here.

def Add_to_Shoping_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checking = ShopCart.objects.filter(
        product_id=id, user_id=current_user.id)

    # print("current user: " + str(current_user.id))
    # print("checking: " + str(checking))
    if checking:
        control = 1
    else:
        control = 0

    if request.method == "POST":
        form = ShopingCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.filter(
                    product_id=id, user_id=current_user.id)
                data.delete()

            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = form.cleaned_data['quantity']
            data.save()
        messages.success(request, 'Your Product  has been added')
        return HttpResponseRedirect(url)
    else:
        if control == 1:
            data = ShopCart.objects.filter(
                product_id=id, user_id=current_user.id)
            data.delete()

        data = ShopCart()
        data.user_id = current_user.id
        data.product_id = id
        data.quantity = 1
        data.save()

        messages.success(request, 'Your  product has been added')
        return HttpResponseRedirect(url)


def cart_details(request):
    categories = Category.objects.all()
    settings = Setting.objects.get(id=1)
    current_user = request.user
    cart_product = ShopCart.objects.filter(user_id=current_user.id)
    totalAmount = 0

    for pro in cart_product:
        totalAmount += pro.product.new_price * pro.quantity

    context = {
        'categories': categories,
        'settings': settings,
        'cart_product': cart_product,
        'totalAmount': totalAmount,

    }

    return render(request, 'shopping_cart.html', context)


def cart_delete(request, id):
    url = request.META.get('HTTP_REFERER')

    current_user = request.user
    cart_product = ShopCart.objects.filter(
        id=id, user_id=current_user.id)
    cart_product.delete()

    messages.warning(request, 'Product item has been deleted')
    return HttpResponseRedirect(url)

#  have to update


@login_required(login_url='/user/login')
def OrderCart(request):
    current_user = request.user
    shoping_cart = ShopCart.objects.filter(user_id=current_user.id)
    totalamount = 0
    for rs in shoping_cart:
        totalamount += rs.quantity*rs.product.new_price
    if request.method == "POST":
        form = OderForm(request.POST, request.FILES)
        if form.is_valid():
            dat = Order()
            # get product quantity from form
            dat.first_name = form.cleaned_data['first_name']
            dat.last_name = form.cleaned_data['last_name']
            dat.address = form.cleaned_data['address']
            dat.city = form.cleaned_data['city']
            dat.phone = form.cleaned_data['phone']
            dat.country = form.cleaned_data['country']
            dat.transaction_id = form.cleaned_data['transaction_id']
            dat.transaction_image = form.cleaned_data['transaction_image']
            dat.user_id = current_user.id
            dat.total = totalamount
            dat.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  # random cod
            dat.code = ordercode
            dat.save()

            # moving data shortcart to product cart
            for rs in shoping_cart:
                data = OderProduct()
                data.order_id = dat.id
                data.product_id = rs.product_id
                data.user_id = current_user.id
                data.quantity = rs.quantity
                data.price = rs.product.new_price
                data.amount = rs.amount
                data.save()

                product = Product.objects.get(id=rs.product_id)
                product.quantity -= rs.quantity
                product.save()
            # Now remove all oder data from the shoping cart
            ShopCart.objects.filter(user_id=current_user.id).delete()
            # request.session['cart_item']=0
            messages.success(request, 'Your oder has been completed')
            categories = Category.objects.all()
            settings = Setting.objects.get(id=1)
            context = {
                # 'category':category,
                'ordercode': ordercode,
                'categories': categories,
                'settings': settings,
            }

            return render(request, 'oder_completed.html', context)
        else:
            messages.warning(request, form.errors)
          #  return HttpResponseRedirect("/order/oder_cart")
    form = OderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    total_amount = 0
    for p in shoping_cart:
        total_amount += p.product.new_price*p.quantity
    categories = Category.objects.all()
    settings = Setting.objects.get(id=1)

    context = {
        # 'category':category,
        'shoping_cart': shoping_cart,
        'totalamount': totalamount,
        'profile': profile,
        'form': form,
        'categories': categories,
        'settings': settings,
        'total_amount': total_amount
    }
    return render(request, 'order_form.html', context)
