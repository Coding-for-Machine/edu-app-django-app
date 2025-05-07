from django.db import models
from lessons.models import Lessons

# Create your models here.
"""
 {
      id: 2,
      title: "Node.js da HTTP server yaratish",
      description: `
        <p>Ushbu vazifada siz Node.js da oddiy HTTP server yaratishingiz kerak bo'ladi.</p>
        <p>Quyidagi qadamlarni bajaring:</p>
        <ol>
          <li>Yangi papka yarating va uni "http-server" deb nomlang</li>
          <li>Shu papka ichida "server.js" nomli fayl yarating</li>
          <li>server.js faylida HTTP server yarating</li>
          <li>Server 3000 portda ishga tushsin</li>
          <li>Server quyidagi yo'nalishlarga javob bersin:</li>
          <ul>
            <li>/ - "Bosh sahifa"</li>
            <li>/about - "Biz haqimizda"</li>
            <li>/contact - "Bog'lanish"</li>
          </ul>
          <li>Serverni ishga tushiring va brauzerda tekshiring</li>
        </ol>
      `,
      requirements: [
        "HTTP server yaratish",
        "3 ta yo'nalish uchun handler yozish",
        "Serverni ishga tushirish va brauzerda tekshirish",
        "Kodni va natijani screenshot qilib yuborish",
      ],
"""

class Tasks(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    requirements = models.TextField()
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    def __str__(self):
        return self.title