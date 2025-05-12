from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=500, blank=True)
    image = models.ImageField(upload_to="category/", blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="instructor_profile")
    title = models.CharField(max_length=200)
    bio = models.TextField()
    avatar = models.ImageField(upload_to="instructor_avatars/", null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.phone_number} - {self.title}"


class Course(models.Model):
    LEVEL_CHOICES = [
        ("Boshlang'ich", "Boshlang'ich"),
        ("O'rta", "O'rta"),
        ("Yuqori", "Yuqori"),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=500, blank=True)
    short_description = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to="course_images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    language = models.CharField(max_length=50, default="O'zbek")
    duration = models.CharField(max_length=50)  # Example: "8 hafta"
    certificate = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="courses")
    students = models.ManyToManyField(User, through="Enrollment", related_name="enrolled_courses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def students_count(self):
        return self.students.count()
    
    @property
    def modules_count(self):
        return self.modules.count()


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'course']


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'course']


@receiver(pre_save, sender=Course)
def courses_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_unique_slug(instance, Course, 'title')
        
@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_unique_slug(instance, Category, "title" )

def create_unique_slug(instance, model, field_name):
    title = getattr(instance, field_name)
    slug = slugify(title, allow_unicode=True)
    if len(slug) > 500:
        slug = slug[:500]
    unique_slug = slug
    counter = 1
    
    while model.objects.filter(slug=unique_slug).exclude(id=instance.id).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1
        if len(unique_slug) > 500:
            unique_slug = f"{slug[:490]}-{counter}"
    
    return unique_slug