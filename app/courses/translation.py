# courses/translation.py
from modeltranslation.translator import TranslationOptions, translator
from .models import Category, Courses  # Category import qilinganligiga ishonch hosil qiling

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # Tarjima qilinadigan maydonlar

translator.register(Category, CategoryTranslationOptions)


class CoursesTranslationOptions(TranslationOptions):
    fields = ('title', 'instructor', 'level', 'duration', 'price')
translator.register(Courses, CoursesTranslationOptions)
