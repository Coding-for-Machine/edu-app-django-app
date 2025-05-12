from django.contrib import admin

# Register your models here.
from .models import Lesson, Module

admin.site.register(Module)
admin.site.register(Lesson)