from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Worker)
admin.site.register(Machine)
admin.site.register(Task)