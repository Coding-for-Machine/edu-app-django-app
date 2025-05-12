from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save
from courses.models import Course, create_unique_slug
from ckeditor_uploader.fields import RichTextUploadingField


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    slug = models.SlugField(blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    slug = models.SlugField(blank=True)
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    video_url = models.URLField(null=True, blank=True)  
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"
    

class LessonImage(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="images")
    url = models.ImageField(upload_to="lesson_images/")
    caption = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Image for {self.lesson.title}"


class LessonAttachment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="attachments")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="lesson_attachments/")
    file_type = models.CharField(max_length=50)  # Example: "PDF", "ZIP"
    
    def __str__(self):
        return f"{self.title} - {self.file_type}"

# segnal 
@receiver(pre_save, sender=Module)
def courses_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_unique_slug(instance, Module, 'title')

@receiver(pre_save, sender=Lesson)
def courses_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_unique_slug(instance, Lesson, 'title')
