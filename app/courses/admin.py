# courses/admin.py
from django.contrib import admin
from .models import Category, Course, Instructor, Enrollment, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class CoursesAdmin(admin.ModelAdmin):
    pass

@admin.register(Instructor)
class CoursesAdmin(admin.ModelAdmin):
    pass

@admin.register(Enrollment)
class CoursesAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class CoursesAdmin(admin.ModelAdmin):
    pass