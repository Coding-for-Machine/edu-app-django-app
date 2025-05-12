from django.shortcuts import get_list_or_404
from ninja import Router
from ninja.errors import HttpError
from typing import List
from .schemas import ModuleListSchemas
from .models import Module


lesson_api_router = Router(tags=["Lesson va Module api"])


@lesson_api_router.get("module/", response=List[ModuleListSchemas])
def module_list_api(request):
    module = Module.objects.all()
    return [
        {
            "id": m.id,
            "title": m.title,
            "description": m.description,
            "order": m.order,
        }
        for m in module
    ]


@lesson_api_router.get("{slug}/", response=List[ModuleListSchemas])
def module_list_api(request, slug: str):
    try:
        module = get_list_or_404(Module, slug=slug)
    except Module.DoesNotExist as err:
        HttpError(404, "Modul topilmadi!")