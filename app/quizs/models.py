from django.db import models
from lessons.models import Module


class Test(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="tests")
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"

    

class Question(models.Model):
    QUESTION_TYPES = [
        ("single-choice", "Single Choice"),
        ("multi-choice", "Multiple Choice"),
        ("text-input", "Text Input"),
    ]
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    correct_answer = models.JSONField()  # For single choice: "a", for multi: ["a", "c"], for text: "answer"
    
    def __str__(self):
        return f"{self.test.title} - Question {self.id}"

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    is_corract = models.BooleanField(default=False)  # Example: "a", "b", "c", "d"
    text = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.question.id} - Option {self.text}"
