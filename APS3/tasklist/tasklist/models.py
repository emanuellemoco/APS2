# pylint: disable=missing-module-docstring,missing-class-docstring
from typing import Optional

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


# pylint: disable=too-few-public-methods

class User(BaseModel):
    username: str = Field(
        title='Username',
        max_length=20,
    )

    class Config:
        schema_extra = {
            'example': {
                'username': 'pessoa1',
            }
        }




class Task(BaseModel):

    username: str = Field(
        'username',
        title='Username',
        max_length = 20,
    )
    description: Optional[str] = Field(
        'no description',
        title='Task description',
        max_length=1024,
    )
    completed: Optional[bool] = Field(
        False,
        title='Shows whether the task was completed',
    )

    class Config:
        schema_extra = {
            'example': {
                'username': 'pessoa1',
                'description': 'Buy baby diapers',
                'completed': False,
            }
        }
