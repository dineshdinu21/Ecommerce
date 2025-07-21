from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.admin_dashboard, name='admin_dashboard'),
    path('user/',views.user,name='user'),
    path('seller/',views.seller,name='seller'),
    path('products/',views.products,name='products'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete-seller/<int:seller_id>/', views.delete_seller, name='delete_seller'),
    path('user/<int:user_id>/activate/', views.activate_user, name='activate_user'),
    path('user/<int:user_id>/deactivate/', views.deactivate_user, name='deactivate_user'),
    path('seller/<int:seller_id>/activate/', views.activate_seller, name='activate_seller'),
    path('seller/<int:seller_id>/deactivate/', views.deactivate_seller, name='deactivate_seller'),
    path('delete/product/<int:product_id>/',views.delete_product,name='delete_product')
]
