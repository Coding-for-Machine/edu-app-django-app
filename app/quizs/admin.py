from django.contrib import admin

# Register your models here.
from .models import Test, Question, Option


admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Option)


