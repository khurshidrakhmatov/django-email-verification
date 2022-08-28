from atexit import register
from django.contrib import admin
from .forms import CustomUserCreationForm
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class UserAdmin(UserAdmin):
      add_form=CustomUserCreationForm
      model = User
      list_display = ( 'first_name', 'username', 'phone_number', "date_joined",  'is_staff', "is_verified", 'web', 'github', "pro")
      fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ( 'phone_number', "bio", "pic", "is_verified", "address", 'web', 'github', "pro")}),
      )
      add_fieldsets = UserAdmin.add_fieldsets + (
        (None,{'fields':( 'phone_number', "bio", "pic", "is_verified", "address", 'web', 'github', "pro")}),
      )



admin.site.register(User, UserAdmin)    
