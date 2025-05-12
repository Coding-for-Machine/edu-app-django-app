from pydantic import BaseModel
from typing import Optional

class InstructorMiniSchema(BaseModel):
    id: int
    user: str
    title: str
    avatar: Optional[str] = None

class CategoryMiniSchema(BaseModel):
    id: int
    name: str
    slug: str
    image: Optional[str] = None

class CourseListSchema(BaseModel):
    id: int
    title: str
    slug: str
    short_description: str
    image: Optional[str]
    level: str
    language: str
    duration: str
    certificate: bool
    featured: bool
    students_count: int
    modules_count: int
    category: CategoryMiniSchema
    instructor: InstructorMiniSchema
