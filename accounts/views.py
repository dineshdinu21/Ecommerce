from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseForbidden
from . models import CustomUser,Products,Cart,PlaceOrder
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from . forms import UserForm,LoginForm,SellerForm,SellerLoginForm,ProductsAddingForm,ResetPasswordForm,PlaceOrderForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.utils import timezone

def homepage(request):
    register_details=CustomUser.objects.all()
    context={"register_details": register_details}
    return render(request,'homepage2.html',context) 

def user_register(request):
    User = get_user_model()
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose another.')
            else:
                user = form.save(commit=False)
                password = form.cleaned_data['password']
                user.set_password(password)
                user.user_type = 'user'
                user.save()
                login(request, user)
                messages.success(request, 'User registered successfully!')
                return redirect('view_user', user_id=user.id)
       
        return render(request, 'user_register.html', {'form': form})
    else:
        form = UserForm()

    return render(request, 'user_register.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None and user.user_type == 'user':
            login(request, user)
            return redirect('view_user', user_id=user.id)

        else:
            messages.error(request,'Incorrect Username or Password')
            form = LoginForm()
            return render(request, 'login.html', {'form': form})
    else:
        form=LoginForm()
    return render(request,'Login.html',{'form':form})


@login_required
def edit_user(request, user_id):
    if request.user.user_type != 'user':
        return HttpResponseForbidden("You cannot edit another user's profile")

    user = request.user

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
    else:
        form = UserForm(instance=user)
    for field in ('password', 'password2','username'):
        form.fields.pop(field, None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('view_user',user_id=user.id)  
    return render(request, 'edit_user.html', {'form': form})


@login_required
def edit_seller(request, seller_id):
    if request.user.user_type != 'seller':
        return HttpResponseForbidden("You cannot edit another seller's profile")

    seller = request.user  

    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES, instance=seller)
    else:
        form = SellerForm(instance=seller)
    for field in ('password', 'password2', 'username'):
        form.fields.pop(field, None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Seller profile updated successfully!')
            return redirect('view_seller', seller_id=seller.id)

    return render(request, 'edit-seller.html', {'form': form})


def seller_register(request):
    User = get_user_model()
    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose another.')
            else:
                seller = form.save(commit=False)
                password = form.cleaned_data['password']
                seller.set_password(password)   
                seller.user_type = 'seller'
                seller.save()
                login(request, seller)
                messages.success(request, 'Seller registered successfully!')
                return redirect('view_seller', seller_id=seller.id)

            return render(request, 'seller_register.html', {'form': form})

    else:
        form = SellerForm()

    return render(request, 'seller_register.html', {'form': form})

def seller_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        seller = authenticate(request, username=username, password=password)
        print(seller)

        if seller is not None and seller.user_type == 'seller':
            login(request, seller)
            return redirect('view_seller', seller_id=seller.id)
        else:
            messages.error(request,'Incorrect Username or Password')
            form = SellerLoginForm()
            return render(request,'seller_login.html', {'form': form})

    else:
        form=SellerLoginForm()
    return render(request,'seller_login.html',{'form':form})


@login_required
def view_user(request,user_id):
    user=get_object_or_404(CustomUser,id=user_id)
    return render(request,'view_user.html', {'user':user})

@login_required
def view_seller(request,seller_id):
    seller=get_object_or_404(CustomUser,id=seller_id)
    return render(request,'view_seller.html', {'seller':seller})

@login_required
def logout_view(request):
    logout(request)
    return redirect('homepage')
    
@login_required
def product_list(request):
    product_details=Products.objects.all()
    context={"product_details":product_details}
    return render(request,'products.html',context)

@login_required
def add_products(request):
    if request.user.user_type!='seller':
        return HttpResponseForbidden("Only sellers can add products.")
    if request.method=='POST':
        form=ProductsAddingForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('view_products')
    else:
        form=ProductsAddingForm() 
    return render(request,'add_products.html',{'form':form})


@login_required
def view_products(request):
    if request.user.user_type != 'seller':
        return HttpResponseForbidden("Only sellers can view their products.")

    products = Products.objects.filter(seller=request.user)
    return render(request, 'view_products.html', {'products': products})


@login_required
def edit_products(request,product_id):
    if request.user.user_type != 'seller':
        return HttpResponseForbidden("Only the required sellers can edit their products.")
    
    product=get_object_or_404(Products,id=product_id,seller=request.user)
    if request.method=='POST':
        form=ProductsAddingForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('view_products')
    else:
        form=ProductsAddingForm(instance=product)
    return render(request,'edit_products.html',{'form':form})

@login_required
def delete_products(request,product_id):
    if request.user.user_type != 'seller':
        return HttpResponseForbidden("Only the required sellers can delete their products.")
    
    product=get_object_or_404(Products,id=product_id,seller=request.user)
    product.delete()
    return redirect('view_products')

@login_required
def reset_password(request,user_id):
    user=get_object_or_404(CustomUser,id=user_id)
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        print(user)
        if form.is_valid():  
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            print(old_password)
            if not user.check_password(old_password):
                print(old_password)
                messages.error(request,'Old password is incorrect.')

            else:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('user_login') 
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})

            
def add_to_cart(request, product_id, user_id):
    if request.user.user_type != 'user':
        messages.error(request, 'Sellers are not allowed to add products to cart.')
        return redirect('homepage')

    product = get_object_or_404(Products, id=product_id)
    user = get_object_or_404(CustomUser, id=user_id)

    if product.stock > 0:
        # Reduce stock
        product.stock -= 1
        product.save()

        # Add or update cart item
        cart_item, created = Cart.objects.get_or_create(user=user, products=product)
        if not created:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1
        cart_item.save()

        messages.success(request, 'This product is added to your cart.')
        return redirect('product_details')
    else:
        messages.error(request, 'This product is out of stock.')
        return redirect('product_details')

def cart_quantity(request,cart_item_id,action):
    if request.method == 'POST':
        cart_items=get_object_or_404(Cart, id=cart_item_id)
        product=cart_items.products
        print(product)

        if action == 'increase':
            if product.stock>0:
                cart_items.quantity+=1
                print('cart')
                product.stock-=1
                cart_items.save()
                product.save()
                print('add1')
            else:
                messages.error(request,'Product is out of stock')
        elif action == 'decrease':
            if cart_items.quantity>1:
                cart_items.quantity-=1
                product.stock+=1
                cart_items.save()
                product.save()
            else:
                messages.error(request,'If you can remove the product click the remove option')
        return redirect('cart_view')
    else:
        return redirect('cart_view')
    
def total_cart(request):
    cart_items=Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    final_total = sum(item.total_amount() for item in cart_items)
    context={
        'cart_items':cart_items,
        'total_price':total_price,
        'final_total':final_total,
    }
    return render(request, 'cart1.html', context)

def calculate_cart_totals(cart_items):
    cart_length = cart_items.count()
    total_price = sum(item.discount_price() for item in cart_items)
    discount_price = sum((item.total_price() - item.discount_price()) for item in cart_items)
    delivery_charge = sum(item.products.delivery_charge for item in cart_items)
    total = sum(item.total_amount() for item in cart_items)
    total_amount = total + cart_length  
    original_price=sum(item.total_price() for item in cart_items)
    print(original_price)

    return {
        'total_price': total_price,
        'discount_price': discount_price,
        'delivery_charge': delivery_charge,
        'total_amount_cart': total_amount,
        'cart_length': cart_length,
        'original_price':original_price
    }



def cart_view(request):
    if request.user.user_type != 'user':
        return HttpResponseForbidden("Sellers are not allowed to view a cart.")

    cart_items = Cart.objects.filter(user=request.user)
    
    cart_total = calculate_cart_totals(cart_items)
    context={
        'cart_items':cart_items,
        **cart_total
    }
    return render(request, 'cart1.html', context)

def place_order(request):
    if request.user.user_type != 'user':
        return HttpResponseForbidden('Only users can place order')

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart_view')
    else:
        print('else')
        last_order = None  

        for item in cart_items:
            last_order = PlaceOrder.objects.create(
                user=request.user,
                product=item.products,
                quantity=item.quantity,
                price=item.total_price()
            )

        cart_items.delete()
        return redirect('order_summary2', order_id=last_order.id)


def remove_cart(request,cart_item_id):
    cart_items=get_object_or_404(Cart,id=cart_item_id)
    cart_items.delete()
    return redirect('cart_view')

def calculate_price(product, quantity):
    price = product.price * quantity
    discount = product.discount
    delivery_charge = product.delivery_charge
    delivery_amount = price + delivery_charge
    discount_amount = price * discount / 100
    discount_price = price - discount_amount
    total_price = int(discount_price + delivery_charge)

    return {
        'price': price,
        'discount_amount': int(discount_amount),
        'discount_price': int(discount_price),
        'total_price_new': total_price,
        'delivery_charge': delivery_charge,
        'delivery_amount': delivery_amount
    }


def buynow_view(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    if product.stock == 0:
        messages.error(request,'This product is currently out of stock.')
        return redirect('product_details')
    quantity = 1

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            print(quantity)
        except ValueError:
            quantity = 1

        if quantity < 1:
            quantity = 1
        elif quantity > product.stock:
            quantity = product.stock
            
    request.session['buy_now_quantity'] = quantity
    stock_range = range(1, product.stock + 1)
    price_details=calculate_price(product,quantity)

    context = {
        'product': product,
        'quantity': quantity,
        'stock_range':stock_range,
        **price_details
    }
    return render(request, 'buynow.html', context)

def place_order_view(request, product_id=None):
    if product_id:
        # Buy Now mode
        product = get_object_or_404(Products, id=product_id)
        quantity = request.session.get('buy_now_quantity', 1)
        cart_items = None
    else:
        # Cart mode
        cart_items = Cart.objects.filter(user=request.user)
        product = None
        quantity = None

    if request.method == 'POST':
        form = PlaceOrderForm(request.POST, user=request.user)
        if form.is_valid():
            address_data = form.cleaned_data  # get address & payment info

            if product_id:
                # Buy Now flow
                order = form.save(commit=False)
                order.user = request.user
                order.mobile = request.user.mobile
                order.product = product
                order.quantity = quantity
                order.price = product.price * quantity
                order.save()
                print("Buy Now order placed.")
                return redirect('order_summary', order_id=order.id)

            else:
                # Cart flow: loop and create orders
                if not cart_items.exists():
                    return redirect('cart_view')

                order_ids = []
                for item in cart_items:
                    order = PlaceOrder.objects.create(
                        user=request.user,
                        mobile=request.user.mobile,
                        product=item.products,
                        quantity=item.quantity,
                        price=item.total_price(),
                        door_no=address_data['door_no'],
                        street_name=address_data['street_name'],
                        city_name=address_data['city_name'],
                        district=address_data['district'],
                        state=address_data['state'],
                        zip_code=address_data['zip_code'],
                        payment_method=address_data['payment_method'],
                    )
                    order_ids.append(order.id)

                # cart_items.delete()
                request.session['recent_order_ids'] = order_ids
                return redirect('/order_summary/?from_cart=1')

        else:
            print('Form is not valid')
            print(form.errors)
    else:
        form = PlaceOrderForm(user=request.user)

    return render(request, 'place_order.html', {
        'form': form,
        'product': product,
        'quantity': quantity,
        'cart_items': cart_items,
        'is_cart': not product_id
    })

def order_summary(request, order_id=None):
    from_cart = request.GET.get('from_cart') == '1'

    if from_cart:
        order_ids = request.session.get('recent_order_ids', [])
        orders = PlaceOrder.objects.filter(id__in=order_ids, user=request.user)
        cart = Cart.objects.filter(user=request.user)
        total_price = sum(order.price for order in orders)
        cart_total=calculate_cart_totals(cart)
        shipping_order=orders.first()
        card_payment = shipping_order.payment_method in ['Credit or Debit']
        upi_payment = shipping_order.payment_method in ['UPI Payment']
        return render(request, 'order_details.html', {
            'cart_items': orders,
            'is_cart': True,
            'order':shipping_order, 
            'grand_total': total_price,
            'make_payment':card_payment,
            'upi_payment':upi_payment,
            **cart_total
        })

    else:
        # 🛍 BUY NOW FLOW
        order = get_object_or_404(PlaceOrder, id=order_id, user=request.user)
       
        product = order.product
        quantity = order.quantity
        price_details = calculate_price(product, quantity)
        price = product.price * quantity
        delivery_charge = product.delivery_charge
        total_price = price + delivery_charge
        card_payment = order.payment_method in ['Credit or Debit']
        upi_payment = order.payment_method in ['UPI Payment']
        return render(request, 'order_details.html', {
            'order': order,
            'is_cart': False,
            'total_price': total_price,
            'make_payment':card_payment,
            'upi_payment':upi_payment,
            'delivery_charge': delivery_charge,
            **price_details
        })



def delete_cart(request, order):
    if order.payment_method in ['Cash on Delivery', 'UPI Payment', 'Card Payment']:
        Cart.objects.filter(user=request.user).delete()


def card_payment(request, order_id):
    from_cart = request.GET.get('from_cart') == '1'
    local_time = timezone.localtime()
    order = get_object_or_404(PlaceOrder, id=order_id, user=request.user)
    cart = Cart.objects.filter(user=request.user)
    
    product = order.product
    quantity = order.quantity
    price_details = calculate_price(product, quantity)
    cart_total={}
    
    if from_cart:
        cart = Cart.objects.filter(user=request.user)
        cart_total = calculate_cart_totals(cart)
    
    if request.method == 'POST':
        delete_cart(request, order)
        return render(request, 'payment_success.html', {
                'order': order,
                **price_details,
                'payment_method': 'UPI_ID Payment',
                'timestamp': local_time,
                **cart_total,
                'is_cart': from_cart
            })

    return render(request, 'card_payment.html', {
        'order': order,
        **price_details,
        **cart_total,
        'is_cart': from_cart
    })


def upi_payment(request, order_id):
    from_cart = request.GET.get('from_cart') == '1'
    local_time = timezone.localtime()
    order = get_object_or_404(PlaceOrder, id=order_id, user=request.user)
    cart = Cart.objects.filter(user=request.user)
    
    product = order.product
    quantity = order.quantity
    price_details = calculate_price(product, quantity)
    cart_total = {}
    if from_cart:
        cart = Cart.objects.filter(user=request.user)
        cart_total = calculate_cart_totals(cart)

    if request.method == 'POST':
        method = request.POST.get('method')

        if method == 'upi':
            upi_id = request.POST.get('upi_id')
            if upi_id:
                delete_cart(request, order)
                return render(request, 'payment_success.html', {
                    'order': order,
                    **price_details,
                    'payment_method': 'UPI_ID Payment',
                    'timestamp': local_time,
                    'message': 'Payment Successful through UPI ID',
                    **cart_total,
                    'is_cart': from_cart
                })
            return render(request, 'upi_id.html')

        else:
            upi_qr = request.POST.get('upi_qr')
            if upi_qr:
                delete_cart(request, order)
                return render(request, 'payment_success.html', {
                    'order': order,
                    **price_details,
                    'payment_method': 'UPI_QR Payment',
                    'timestamp': local_time,
                    'message': 'Payment Successful through UPI QR',
                    **cart_total,
                    'is_cart': from_cart
                })
            return render(request, 'upi_qr.html')

    return render(request, 'upi_payment.html', {
        'order': order,
        **price_details,
        **cart_total,
        'is_cart': from_cart
    })

def order_successfull(request,order_id):
    from_cart = request.GET.get('from_cart') == '1'
    local_time = timezone.localtime()
    order = get_object_or_404(PlaceOrder, id=order_id, user=request.user)
    cart = Cart.objects.filter(user=request.user)
    
    product = order.product
    quantity = order.quantity
    price_details = calculate_price(product, quantity)
    cart_total={}
    
    if from_cart:
        cart = Cart.objects.filter(user=request.user)
        cart_total = calculate_cart_totals(cart)
        delete_cart(request, order)
    
    if request.method == 'POST':
        return render(request, 'order_success.html', {
                'order': order,
                **price_details,
                'timestamp': local_time,
                **cart_total,
                'is_cart': from_cart,
                'payment_method':order.payment_method,
            })
    return render(request, 'order_successfull.html', {
        'order': order,
        **price_details,
        **cart_total,
        'timestamp': local_time,
        'is_cart': from_cart,
        'payment_method':order.payment_method,
    })
        
def order_history(request):
    orders = PlaceOrder.objects.filter(user=request.user).order_by('-id')  # All products ordered by user

    return render(request, 'order_history.html', {
        'orders': orders,
        'status':'Completed'
    })
def clear_order_history(request):
    PlaceOrder.objects.filter(user=request.user).delete()
    return redirect('order_history') 

def about(request):
    return render(request,'about.html')