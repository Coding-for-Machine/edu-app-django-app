# courses/admin.py
from django.contrib import admin
from .models import Category, Courses


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    pass