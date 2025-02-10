from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

from apps.dependencies import Container

container = Container()
router = APIRouter()


@router.get("/ui", include_in_schema=False)
@inject
def custom_swagger_ui():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Swagger UI")


@router.on_event("startup")
async def startup_event():
    container.wire(modules=[__name__])


@router.on_event("shutdown")
async def shutdown_event():
    container.unwire()
