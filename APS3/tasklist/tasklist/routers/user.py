# pylint: disable=missing-module-docstring, missing-function-docstring, invalid-name
import uuid

from typing import Dict

from fastapi import APIRouter, HTTPException, Depends

from ..database import DBSession, get_db
from ..models import User

router = APIRouter()



@router.get(
    '',
    summary='Reads user list',
    description='Reads the whole user list.',
    response_model= list,
)
async def read_tasks(db: DBSession = Depends(get_db)):
    return db.read_users()


@router.post(
    '',
    summary='Creates a new user',
    description='Creates a new user and return its user ',
    response_model=User,
)
async def create_user( user : User, db: DBSession = Depends(get_db)):
    try:
        return db.create_user(user)
    
    except ValueError as exception:
        raise HTTPException(
            status_code=409,
            detail='Username not available',
        ) from exception


@router.put(
    '/{username}',
    summary='Replaces an user',
    description='Replaces an user identified by its username.',
)
async def replace_task(
        username: str,
        user: User,
        db: DBSession = Depends(get_db),
):
    try:
        db.replace_user(username, user)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        ) from exception
    except ValueError as exception:
        raise HTTPException(
            status_code=409,
            detail='New username not available',
        ) from exception


#Qual a diferença entre o patch e o put nesse caso?
@router.patch(
    '/{username}',
    summary='Alters an user',
    description='Alters an user identified by its username.',
)
async def replace_task(
        username: str,
        user: User,
        db: DBSession = Depends(get_db),
):
    try:
        db.replace_user(username, user)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        ) from exception
    except ValueError as exception:
        raise HTTPException(
            status_code=409,
            detail='New username not available',
        ) from exception
    
@router.delete(
    '/{username}',
    summary='Deletes user',
    description='Deletes an user identified by its username',
)
async def remove_task(        
        username: str,
        db: DBSession = Depends(get_db),
):
    try:
        db.remove_user(username)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        ) from exception
