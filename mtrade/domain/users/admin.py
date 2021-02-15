import uuid

from django.contrib import admin

from .models import User, UserID

class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.id = UserID().id
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)

