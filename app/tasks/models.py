from django.db import models
from lessons.models import Module


class Assignment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"
