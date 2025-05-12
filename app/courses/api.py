from ninja  import Router
from typing import List
from .schimas import *
from .models import Category, Instructor, Course

course_router_api = Router(tags=["course api"])
# course api

@course_router_api.get("category/", response=List[CategoryMiniSchema])
def category_api_list(request):
    category = Category.objects.all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "image": c.image
        }
        for c in category
    ]

@course_router_api.get("instructor/", response=List[InstructorMiniSchema])
def instructor_api_list(request):
    instructors = Instructor.objects.all()
    
    # Model obyektlarini Schema formatiga o'tkazish
    return [
        {
            "id": instructor.id,
            "user": str(instructor.user),  # User obyektini string formatga o'tkazish
            "title": instructor.title,
            "bio": instructor.bio,
            "avatar": request.build_absolute_uri(instructor.avatar.url)
        } for instructor in instructors
    ]
@course_router_api.get("/", response=List[CourseListSchema])
def course_list_api(request):
    courses = Course.objects.select_related('instructor__user', 'category').all()

    return [
        {
            "id": course.id,
            "title": course.title,
            "slug": course.slug,
            "short_description": course.short_description,
            "image": request.build_absolute_uri(course.image.url) if course.image else None,
            "level": course.level,
            "language": course.language,
            "duration": course.duration,
            "certificate": course.certificate,
            "featured": course.featured,
            "students_count": course.students_count,
            "modules_count": course.modules_count,

            "category": {
                "id": course.category.id,
                "name": course.category.name,
                "slug": course.category.slug,
                "image": request.build_absolute_uri(course.category.image.url) if course.category.image else None
            },

            "instructor": {
                "id": course.instructor.id,
                "user": str(course.instructor.user),
                "title": course.instructor.title,
                "avatar": request.build_absolute_uri(course.instructor.avatar.url) if course.instructor.avatar else None
            }
        }
        for course in courses
    ]
