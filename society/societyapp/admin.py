from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(News)
admin.site.register(Guest)
admin.site.register(Visitors)
admin.site.register(Complain)
