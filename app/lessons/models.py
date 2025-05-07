from django.db import models

from courses.models import Bob

# Create your models here.
"""
id: 1,
      title: "Node.js ga kirish",
      content: `
        <h2>Node.js nima?</h2>
        <p>Node.js - bu Chrome V8 JavaScript engine asosida qurilgan server tomonidagi platforma. U event-driven, non-blocking I/O modelidan foydalanadi, bu esa uni yengil va samarali qiladi.</p>
        
        <h3>Node.js ning afzalliklari:</h3>
        <ul>
          <li>Asynchronous va Event Driven</li>
          <li>Juda tez</li>
          <li>Single Threaded lekin yuqori darajada scalable</li>
          <li>Buffersiz</li>
          <li>Litsenziya</li>
        </ul>
        
        <h3>Node.js qachon ishlatiladi?</h3>
        <p>Node.js quyidagi hollarda ishlatiladi:</p>
        <ul>
          <li>I/O bound Applications</li>
          <li>Data Streaming Applications</li>
          <li>Data Intensive Real-time Applications (DIRT)</li>
          <li>JSON APIs based Applications</li>
          <li>Single Page Applications</li>
        </ul>
      `,
      type: "video",
      duration: "45 daqiqa",
      hasTest: true,
      hasTask: false,
      completed: false,
    },
    """

class Lessons(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    bob = models.ForeignKey(Bob, on_delete=models.CASCADE)
    # hasTest = models.BooleanField(default=False)
    # hasTask = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title