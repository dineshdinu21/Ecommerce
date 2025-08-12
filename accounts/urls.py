from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('register/user/', views.user_register, name='user_register'),
    path('login/user/', views.user_login, name='user_login'),
    path('register/seller/', views.seller_register, name='seller_register'),
    path('login/seller/', views.seller_login, name='seller_login'),
    path('view_user/<int:user_id>/',views.view_user,name='view_user'),
    path('view_seller/<int:seller_id>/',views.view_seller,name='view_seller'),
    path('logout',views.logout_view,name='logout'),
    path('seller/add_products/', views.add_products, name='add_products'),
    path('view_products/',views.view_products,name='view_products'),
    path('product_details/',views.product_list,name='product_details'),
    path('edit_products/<int:product_id>/',views.edit_products,name='edit_products'),
    path('delete_products/<int:product_id>/',views.delete_products,name='delete_products'),
    path('reset-password/<int:user_id>/',views.reset_password,name='reset_password'),
    path('cart/<int:product_id>/<int:user_id>/', views.add_to_cart, name='cart'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('cart/quantity/<int:cart_item_id>/<str:action>/', views.cart_quantity, name='cart_quantity'),
    path('cart/remove_products/<int:cart_item_id>/',views.remove_cart,name='remove_products'),
    path('buynow/<int:product_id>/', views.buynow_view, name='buynow'),
    # path('place_order/<int:product_id>/', views.place_order_view, name='place_order'),
    # path('order_summary/<int:order_id>/', views.order_details, name='order_summary'),
    path('make-payment/card/<int:order_id>/', views.card_payment, name='make_payment'),
    path('make-payment/upi/<int:order_id>/', views.upi_payment, name='upi_payment'),
    path('order/successfull/<int:order_id>/', views.order_successfull, name='order_successfull'),
    # path('cart/place_order/',views.place_order,name='cart_place_order'),
    
    path('orders/history/', views.order_history, name='order_history'),
    path('place_order/', views.place_order_view, name='cart_place_order'),  # Cart
    path('place_order/<int:product_id>/', views.place_order_view, name='place_order'),  # Buy Now
    path('order_summary/', views.order_summary, name='order_summary_cart'),           # Cart flow
    path('order_summary/<int:order_id>/', views.order_summary, name='order_summary'), # Buy now flow
    path('clear_history/',views.clear_order_history,name='delete_history'),
    path('edit-user/<int:user_id>/',views.edit_user, name='edit_user'),
    path('edit-seller/<int:seller_id>/',views.edit_seller,name='edit_seller'),
    path('about/',views.about,name='about')
]
