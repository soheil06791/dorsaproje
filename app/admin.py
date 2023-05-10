from django.contrib import admin
from .models import DataModel, BlockIp
from django.contrib.auth.hashers import check_password


# Register your models here.

admin.site.register(DataModel)


class AdminPermissoin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser: 
            return True
        return False
    
    def has_add_permission(self, request):
        return False # disable add view
    
    def has_change_permission(self, request, obj=None):
        return False # disable change view

admin.site.register(BlockIp, AdminPermissoin)
