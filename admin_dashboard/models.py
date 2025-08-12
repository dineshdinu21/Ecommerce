from django.db import models

# Create your models here.
# admin_dashboard/models.py

class AdminLog(models.Model):
    action = models.CharField(max_length=100)
    performed_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
