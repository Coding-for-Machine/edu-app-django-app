from ninja import Schema
from typing import List, Optional

class ModuleListSchemas(Schema):
    id: int
    course_id: int
    title: str
    description: str
    order: int


class LessonSchemasList(Schema):
    id: int
    module_id: int
    title: str
    content: str
    video_url: str
    order: int

class LessonImageSchemasList(Schema):
    id: str
    url: str
    caption: str
    


class LessonAttachmentSchemasList(Schema):
    lesson_id: int
    title: str
    file: str
    file_type: str


