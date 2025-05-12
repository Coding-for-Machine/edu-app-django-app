from django.db import models

from lessons.models import Lesson
from quizs.models import Test
from tasks.models import Assignment
from users.models import User

# Create your models here.
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True)  # For tests
    completed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = [
            ['user', 'lesson'],
            ['user', 'test'],
            ['user', 'assignment'],
        ]


class TestSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answers = models.JSONField()  # Store user answers
    score = models.FloatField()
    feedback = models.JSONField()  # Store feedback for each question
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'test']


class AssignmentSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="assignment_submissions/", null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    grade = models.FloatField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'assignment']
