from django.db import models
from lessons.models import Lessons
# Create your models here.
"""
{
      id: 4,
      title: "Node.js umumiy test",
      description: "Bu testda Node.js haqidagi umumiy bilimlaringizni tekshirasiz.",
      questions: [
        {
          id: 1,
          text: "Node.js qaysi tilda yozilgan?",
          answers: [
            { id: 1, text: "JavaScript" },
            { id: 2, text: "C++" },
            { id: 3, text: "Java" },
            { id: 4, text: "Python" },
          ],
          correctAnswer: 2,
        },
"""

class Quizs(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
class Questions(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(Quizs, on_delete=models.CASCADE)
    def __str__(self):
        return self.text[:30]
    
class Answers(models.Model):
    text = models.TextField()
    is_corract = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text
    