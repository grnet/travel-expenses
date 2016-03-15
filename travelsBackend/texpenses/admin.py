from django.contrib import admin

# Register your models here.

from .models import User
from .models import Account
from .models import Specialty

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Specialty)
