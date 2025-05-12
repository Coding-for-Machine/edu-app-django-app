from django.contrib import admin

# Register your models here.
from .models import UserProgress, TestSubmission, AssignmentSubmission

admin.site.register(UserProgress)
admin.site.register(TestSubmission)
admin.site.register(AssignmentSubmission)
