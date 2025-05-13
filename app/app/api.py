from ninja_extra import NinjaExtraAPI
# from ninja.security import HttpBearer
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
# from django.contrib.auth.models import User
# from django.http import HttpRequest
# from ninja.errors import HttpError

# # JWT validatsiya qiluvchi class
# class AuthBearer(HttpBearer):
#     def authenticate(self, request: HttpRequest, token: str):
#         user = JWTAuth().authenticate(request, token)
#         if user is None:
#             raise HttpError(401, "Token noto‘g‘ri yoki muddati tugagan")
#         return user  # bu user ni request.auth sifatida beradi

# # API yaratish
# api = NinjaExtraAPI(
#     title="Course api",
#     docs_url="/docs-api",
#     version="1.0.0",
#     description="Juda Kuchli api",
#     docs_decorator=None)

# # JWT uchun default controller: /api/token/, /api/token/refresh/
# api.register_controllers(NinjaJWTDefaultController)

# from courses.api import course_router_api
# from lessons.api import lesson_api_router
# # app conterol api router 
# api.add_router("course/", course_router_api)
# api.add_router("lesson/", lesson_api_router)


from typing import List, Optional, Dict, Any
from datetime import datetime
from ninja import NinjaAPI, Schema, File
from ninja.files import UploadedFile
from ninja.security import HttpBearer
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count
from courses.models import (
    Category, Course
)
from lessons.models import *
from quizs.models import *
from results.models import *
from tasks.models import *


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        # In a real app, validate the token
        # For demo just returning the token as the user ID
        return token

api = NinjaExtraAPI(
    title="Course api",
    docs_url="/docs-api",
    version="1.0.0",
    description="Juda Kuchli api",
    docs_decorator=None)

api.register_controllers(NinjaJWTDefaultController)

# Schema definitions
class CategorySchema(Schema):
    id: int
    name: str
    slug: str
    image: Optional[str] = None


class InstructorSchema(Schema):
    id: int
    title: str
    bio: str
    avatar: Optional[str] = None
    name: str  # This will come from user.get_full_name()


class CourseListSchema(Schema):
    id: int
    title: str
    short_description: str
    image: str
    category: str
    level: str
    duration: str
    students_count: int
    rating: Optional[float] = None
    reviews_count: int
    featured: bool


class ModuleBasicSchema(Schema):
    id: int
    title: str
    description: str


class LessonBasicSchema(Schema):
    id: int
    title: str
    completed: bool


class TestBasicSchema(Schema):
    id: int
    title: str
    completed: bool


class AssignmentBasicSchema(Schema):
    id: int
    title: str
    completed: bool


class ModuleDetailSchema(Schema):
    id: int
    title: str
    description: str
    completed: bool
    lessons: List[LessonBasicSchema]
    tests: List[TestBasicSchema]
    assignments: List[AssignmentBasicSchema]


class CourseStructureSchema(Schema):
    modules: List[ModuleDetailSchema]


class LessonImageSchema(Schema):
    url: str
    caption: str


class LessonAttachmentSchema(Schema):
    title: str
    url: str
    type: str
    size: str  # We'll format this in the resolver


class LessonDetailSchema(Schema):
    id: int
    title: str
    content: str
    completed: bool
    video_url: Optional[str] = None
    images: List[LessonImageSchema]
    attachments: List[LessonAttachmentSchema]


class OptionSchema(Schema):
    id: str  # 'a', 'b', etc
    text: str


class QuestionSchema(Schema):
    id: str
    text: str
    type: str
    options: List[OptionSchema]


class TestDetailSchema(Schema):
    id: int
    title: str
    description: str
    questions: List[QuestionSchema]


class AssignmentDetailSchema(Schema):
    id: int
    title: str
    description: str
    due_date: Optional[datetime] = None
    completed: bool


class CourseDetailSchema(Schema):
    id: int
    title: str
    description: str
    image: str
    category: str
    level: str
    language: str
    duration: str
    students_count: int
    rating: Optional[float] = None
    reviews_count: int
    modules_count: int
    certificate: bool
    updated_at: datetime
    instructor: InstructorSchema
    modules: List[ModuleBasicSchema]


class SubmitTestSchema(Schema):
    answers: Dict[str, Any]


class TestResultSchema(Schema):
    score: float
    feedback: Dict[str, str]


class SubmitAssignmentSchema(Schema):
    content: Optional[str] = None
    # File will be handled separately


class AssignmentSubmissionResultSchema(Schema):
    success: bool
    feedback: str


class LessonCompleteResultSchema(Schema):
    success: bool


# API Endpoints
@api.get("/categories", response=List[CategorySchema])
def get_categories(request):
    return [
        {
            "id": c.id,
            "name": c.name,
            "image": request.build_absolute_uri(c.image.url) if c.image else None,
            "slug": c.slug,
        }
        for c in Category.objects.all()
    ]


@api.get("/courses/featured", response=List[CourseListSchema])
def get_featured_courses(request):
    courses = Course.objects.filter(featured=True)
    return _prepare_courses_list(request, courses)


@api.get("/courses", response=List[CourseListSchema])
def get_all_courses(request, category: Optional[str] = None):
    courses = Course.objects.all()
    if category:
        courses = courses.filter(category__name=category)
    return _prepare_courses_list(request, courses)


@api.get("/courses/{course_id}", response=CourseDetailSchema)
def get_course_details(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    # Get instructor data
    instructor_data = {
        "id": course.instructor.id,
        "title": course.instructor.title,
        "bio": course.instructor.bio,
        "avatar": request.build_absolute_uri(course.instructor.avatar.url) if course.instructor.avatar else None,
        "name": course.instructor.user.username if course.instructor.user.username else course.instructor.user.phone_number,
    }
    
    # Get course modules
    modules_data = [
        {
            "id": module.id,
            "title": module.title,
            "description": module.description,
        }
        for module in course.modules.all().order_by('order')
    ]
    
    # Get aggregated review data
    reviews_data = course.reviews.aggregate(
        avg_rating=Avg('rating'),
        count=Count('id')
    )
    
    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "image": course.image.url,
        "category": course.category.name,
        "level": course.level,
        "language": course.language,
        "duration": course.duration,
        "students_count": course.students_count,
        "rating": reviews_data['avg_rating'],
        "reviews_count": reviews_data['count'],
        "modules_count": course.modules_count,
        "certificate": course.certificate,
        "updated_at": course.updated_at,
        "instructor": instructor_data,
        "modules": modules_data,
    }


@api.get("/courses/{course_id}/structure", response=CourseStructureSchema, auth=AuthBearer())
def get_course_structure(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    user = request.auth  # In real app, get user from token
    
    modules_data = []
    for module in course.modules.all().order_by('order'):
        # Check if module is completed by checking if all lessons are completed
        module_completed = all(
            UserProgress.objects.filter(user=user, lesson=lesson, completed=True).exists()
            for lesson in module.lessons.all()
        )
        
        # Get lessons with completion status
        lessons_data = []
        for lesson in module.lessons.all().order_by('order'):
            lesson_completed = UserProgress.objects.filter(
                user=user, lesson=lesson, completed=True
            ).exists()
            lessons_data.append({
                "id": lesson.id,
                "title": lesson.title,
                "completed": lesson_completed,
            })
        
        # Get tests with completion status
        tests_data = []
        for test in module.tests.all():
            test_completed = UserProgress.objects.filter(
                user=user, test=test, completed=True
            ).exists()
            tests_data.append({
                "id": test.id,
                "title": test.title,
                "completed": test_completed,
            })
        
        # Get assignments with completion status
        assignments_data = []
        for assignment in module.assignments.all():
            assignment_completed = UserProgress.objects.filter(
                user=user, assignment=assignment, completed=True
            ).exists()
            assignments_data.append({
                "id": assignment.id,
                "title": assignment.title,
                "completed": assignment_completed,
            })
        
        modules_data.append({
            "id": module.id,
            "title": module.title,
            "description": module.description,
            "completed": module_completed,
            "lessons": lessons_data,
            "tests": tests_data,
            "assignments": assignments_data,
        })
    
    return {"modules": modules_data}


@api.get("/courses/{course_id}/modules/{module_id}", response=ModuleDetailSchema, auth=AuthBearer())
def get_module_details(request, course_id: int, module_id: int):
    module = get_object_or_404(Module, id=module_id, course_id=course_id)
    user = request.auth  # In real app, get user from token
    
    # Check if module is completed
    module_completed = all(
        UserProgress.objects.filter(user=user, lesson=lesson, completed=True).exists()
        for lesson in module.lessons.all()
    )
    
    # Get lessons with completion status
    lessons_data = []
    for lesson in module.lessons.all().order_by('order'):
        lesson_completed = UserProgress.objects.filter(
            user=user, lesson=lesson, completed=True
        ).exists()
        lessons_data.append({
            "id": lesson.id,
            "title": lesson.title,
            "completed": lesson_completed,
        })
    
    # Get tests with completion status
    tests_data = []
    for test in module.tests.all():
        test_completed = UserProgress.objects.filter(
            user=user, test=test, completed=True
        ).exists()
        tests_data.append({
            "id": test.id,
            "title": test.title,
            "completed": test_completed,
        })
    
    # Get assignments with completion status
    assignments_data = []
    for assignment in module.assignments.all():
        assignment_completed = UserProgress.objects.filter(
            user=user, assignment=assignment, completed=True
        ).exists()
        assignments_data.append({
            "id": assignment.id,
            "title": assignment.title,
            "completed": assignment_completed,
        })
    
    return {
        "id": module.id,
        "title": module.title,
        "description": module.description,
        "completed": module_completed,
        "lessons": lessons_data,
        "tests": tests_data,
        "assignments": assignments_data,
    }


@api.get("/courses/{course_id}/modules/{module_id}/lessons/{lesson_id}", response=LessonDetailSchema, auth=AuthBearer())
def get_lesson_content(request, course_id: int, module_id: int, lesson_id: int):
    lesson = get_object_or_404(
        Lesson, 
        id=lesson_id, 
        module_id=module_id, 
        module__course_id=course_id
    )
    user = request.auth  # In real app, get user from token
    
    # Check if lesson is completed
    lesson_completed = UserProgress.objects.filter(
        user=user, lesson=lesson, completed=True
    ).exists()
    
    # Get lesson images
    images_data = [
        {
            "url": image.url.url,
            "caption": image.caption,
        }
        for image in lesson.images.all()
    ]
    
    # Get lesson attachments
    attachments_data = [
        {
            "title": attachment.title,
            "url": attachment.file.url,
            "type": attachment.file_type,
            "size": f"{attachment.file.size / (1024 * 1024):.1f} MB",  # Format size in MB
        }
        for attachment in lesson.attachments.all()
    ]
    
    return {
        "id": lesson.id,
        "title": lesson.title,
        "content": lesson.content,
        "completed": lesson_completed,
        "video_url": lesson.video_url,
        "images": images_data,
        "attachments": attachments_data,
    }


@api.get("/courses/{course_id}/modules/{module_id}/tests/{test_id}", response=TestDetailSchema, auth=AuthBearer())
def get_test_content(request, course_id: int, module_id: int, test_id: int):
    test = get_object_or_404(
        Test, 
        id=test_id, 
        module_id=module_id, 
        module__course_id=course_id
    )
    
    questions_data = []
    for question in test.questions.all():
        options_data = [
            {
                "id": option.option_id,
                "text": option.text,
            }
            for option in question.options.all()
        ]
        
        questions_data.append({
            "id": str(question.id),
            "text": question.text,
            "type": question.type,
            "options": options_data,
        })
    
    return {
        "id": test.id,
        "title": test.title,
        "description": test.description,
        "questions": questions_data,
    }


@api.get("/courses/{course_id}/modules/{module_id}/assignments/{assignment_id}", 
         response=AssignmentDetailSchema, auth=AuthBearer())
def get_assignment_content(request, course_id: int, module_id: int, assignment_id: int):
    assignment = get_object_or_404(
        Assignment, 
        id=assignment_id, 
        module_id=module_id, 
        module__course_id=course_id
    )
    user = request.auth  # In real app, get user from token
    
    # Check if assignment is completed
    assignment_completed = UserProgress.objects.filter(
        user=user, assignment=assignment, completed=True
    ).exists()
    
    return {
        "id": assignment.id,
        "title": assignment.title,
        "description": assignment.description,
        "due_date": assignment.due_date,
        "completed": assignment_completed,
    }


@api.post("/courses/{course_id}/modules/{module_id}/lessons/{lesson_id}/complete", 
          response=LessonCompleteResultSchema, auth=AuthBearer())
def mark_lesson_complete(request, course_id: int, module_id: int, lesson_id: int):
    lesson = get_object_or_404(
        Lesson, 
        id=lesson_id, 
        module_id=module_id, 
        module__course_id=course_id
    )
    user = request.auth  # In real app, get user from token
    
    # Mark lesson as completed
    progress, created = UserProgress.objects.get_or_create(
        user=user,
        lesson=lesson,
        defaults={"completed": True}
    )
    
    if not created:
        progress.completed = True
        progress.save()
    
    return {"success": True}


@api.post("/courses/{course_id}/modules/{module_id}/tests/{test_id}/submit", 
          response=TestResultSchema, auth=AuthBearer())
def submit_test(request, course_id: int, module_id: int, test_id: int, data: SubmitTestSchema):
    test = get_object_or_404(
        Test, 
        id=test_id, 
        module_id=module_id, 
        module__course_id=course_id
    )
    user = request.auth  # In real app, get user from token
    
    # Calculate score and generate feedback
    total_questions = test.questions.count()
    correct_answers = 0
    feedback = {}
    
    for question in test.questions.all():
        question_id = str(question.id)
        if question_id in data.answers:
            user_answer = data.answers[question_id]
            correct_answer = question.correct_answer
            
            is_correct = False
            if question.type == "single-choice":
                is_correct = user_answer == correct_answer
            elif question.type == "multi-choice":
                is_correct = set(user_answer) == set(correct_answer)
            elif question.type == "text-input":
                is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
            
            if is_correct:
                correct_answers += 1
                feedback[question_id] = "To'g'ri!"
            else:
                feedback[question_id] = "Noto'g'ri. Qayta urinib ko'ring."
    
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    # Save test submission
    test_submission = TestSubmission.objects.create(
        user=user,
        test=test,
        answers=data.answers,
        score=score,
        feedback=feedback
    )
    
    # Mark test as completed in user progress
    UserProgress.objects.update_or_create(
        user=user,
        test=test,
        defaults={"completed": True, "score": score}
    )
    
    return {
        "score": score,
        "feedback": feedback,
    }


@api.post("/courses/{course_id}/modules/{module_id}/assignments/{assignment_id}/submit", 
          response=AssignmentSubmissionResultSchema)
def submit_assignment(
    request, 
    course_id: int, 
    module_id: int, 
    assignment_id: int, 
    content: Optional[str] = None,
    file: Optional[UploadedFile] = File(None)
):
    assignment = get_object_or_404(
        Assignment, 
        id=assignment_id, 
        module_id=module_id, 
        module__course_id=course_id
    )
    user = request.auth  # In real app, get user from token
    
    # Create or update assignment submission
    submission, created = AssignmentSubmission.objects.update_or_create(
        user=user,
        assignment=assignment,
        defaults={
            "content": content,
            "file": file,
        }
    )
    
    # Mark assignment as submitted in user progress
    UserProgress.objects.update_or_create(
        user=user,
        assignment=assignment,
        defaults={"completed": True}
    )
    
    return {
        "success": True,
        "feedback": "Vazifangiz qabul qilindi. Tez orada tekshirilib, natija e'lon qilinadi.",
    }


# Helper functions
def _prepare_courses_list(request, courses):
    result = []
    for course in courses:
        # Get aggregated review data
        reviews_data = course.reviews.aggregate(
            avg_rating=Avg('rating'),
            count=Count('id')
        )
        
        result.append({
            "id": course.id,
            "title": course.title,
            "short_description": course.short_description,
            "image": request.build_absolute_uri(course.image.url) if course.image else None,
            "category": course.category.name,
            "level": course.level,
            "duration": course.duration,
            "students_count": course.students_count,
            "rating": reviews_data['avg_rating'],
            "reviews_count": reviews_data['count'],
            "featured": course.featured,
        })
    
    return result