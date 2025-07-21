from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from . models import CustomUser,Products,Cart,PlaceOrder

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'mobile', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('mobile', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('mobile', 'address')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(PlaceOrder)