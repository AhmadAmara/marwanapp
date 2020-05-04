from django.contrib import admin

# Register your models here.
from .models import User
admin.site.register(User)

from .models import Order
admin.site.register(Order)

from .models import ActiveOrder
admin.site.register(ActiveOrder)
