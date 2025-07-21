# admin_dashboard/admin.py

from django.contrib import admin
from . models import AdminLog

admin.site.register(AdminLog)
