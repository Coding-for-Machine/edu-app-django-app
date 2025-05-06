# courses/admin.py
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Category, Courses
@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    pass

@admin.register(Courses)
class CoursesAdmin(TranslationAdmin):
    pass