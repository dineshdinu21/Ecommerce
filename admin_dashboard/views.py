from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import CustomUser,Products
from django.utils.safestring import mark_safe
import re

def admin_dashboard(request):
    users = CustomUser.objects.filter(user_type='user')
    sellers = CustomUser.objects.filter(user_type='seller')
    products= Products.objects.all()
    q_user = request.GET.get('q')
    q_product = request.GET.get('q_product')

    if q_user:
        users = users.filter(username__icontains=q_user)
        sellers = sellers.filter(username__icontains=q_user)
        for user in users:
            if q_user:
                user.highlighted_username = user.username.lower().replace(
                    q_user.lower(), f'<span style="background-color: yellow;">{q_user}</span>'
                )
            else:
                user.highlighted_username = user.username
    if q_product:
        products = products.filter(product_name__icontains=q_product)

    return render(request, 'admin.html', {
        'users': users,
        'sellers': sellers,
        'products':products,
    })


def user(request):
    q_user = request.GET.get('q')
    users = CustomUser.objects.filter(user_type='user')
    if q_user:
        users = users.filter(username__icontains=q_user)

    for user in users:
        if q_user:
           
            pattern = re.compile(re.escape(q_user), re.IGNORECASE)
            highlighted = pattern.sub(
                lambda m: f'<span style="background-color: yellow;">{m.group(0)}</span>',
                user.username
            ) 
            user.highlighted_username = mark_safe(highlighted)
        else:
     
            user.highlighted_username = user.username

    return render(request, 'admin-user.html', {'users': users})



def seller(request):
    q_seller = request.GET.get('q')
    sellers = CustomUser.objects.filter(user_type='seller')
    if q_seller:
        sellers = sellers.filter(username__icontains=q_seller)
        
    for seller in sellers:
        if q_seller:
           
            pattern = re.compile(re.escape(q_seller), re.IGNORECASE)
            highlighted = pattern.sub(
                lambda m: f'<span style="background-color: yellow;">{m.group(0)}</span>',
                seller.username
            )
            seller.highlighted_username = mark_safe(highlighted)
        else:
     
            seller.highlighted_username = seller.username

    return render(request, 'admin-seller.html', {'sellers': sellers})

def products(request):
    q_products = request.GET.get('q_product')
    products = Products.objects.all()

    if q_products:
        products = products.filter(product_name__icontains=q_products)

    for product in products:
        if q_products:
            pattern = re.compile(re.escape(q_products), re.IGNORECASE)
            highlighted = pattern.sub(
                lambda m: f'<span style="background-color: yellow;">{m.group(0)}</span>',
                product.product_name
            )
            product.highlighted_productname = mark_safe(highlighted)
        else:
            product.highlighted_productname = product.product_name

    return render(request, 'admin-products.html', {'products': products})




def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('seller')

def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    return redirect('user')  

def deactivate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False
    user.save()
    return redirect('user')

#seller

def activate_seller(request, seller_id):
    user = get_object_or_404(CustomUser, id=seller_id)
    user.is_active = True
    user.save()
    return redirect('seller')  

def deactivate_seller(request, seller_id):
    user = get_object_or_404(CustomUser, id=seller_id)
    user.is_active = False
    user.save()
    return redirect('seller')

def delete_seller(request,seller_id):
    seller=get_object_or_404(CustomUser,id=seller_id)
    seller.delete()
    return redirect('seller')

#products

def delete_product(request,product_id):
    product=get_object_or_404(Products,id=product_id)
    product.delete()
    return redirect('products')