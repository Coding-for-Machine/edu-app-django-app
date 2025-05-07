from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=60)
    def __str__(self):
        return str(self.name)
    

"""
{
    id: 1,
    title: "Node.js va Express orqali backend dasturlash",
    instructor: "Azimjon Po'latov",
    category: "Backend",
    level: "O'rta",
    students: 1250,
    duration: "12 hafta",
    price: "Bepul",
    image: "/placeholder.svg?height=200&width=400",
},
"""
class Courses(models.Model):
    title = models.CharField(max_length=250, help_text="Sarlavha")
    instructor = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.CharField(max_length=20)
    # students = 
    duration = models.CharField(max_length=60, help_text="12 hafta")
    price = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to="courses/")
    def __str__(self):
        return str(self.title)
    
class Bob(models.Model):
    title = models.CharField(max_length=60)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    def __str__(self):
        return self.title