# pylint: disable=missing-module-docstring
from fastapi import FastAPI

from .routers import task

from .routers import user


tags_metadata = [
    {
        'name': 'user',
        'description': 'Operations related to users.',
    },
    {
        'name': 'task',
        'description': 'Operations related to tasks.',
    },


]
#uwu
app = FastAPI(
    title='Task list',
    description='Task-list project for the **Megadados** course',
    openapi_tags=tags_metadata,
)

app.include_router(user.router, prefix='/user', tags=['user'])
app.include_router(task.router, prefix='/task', tags=['task'])


