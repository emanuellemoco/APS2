# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import json
import uuid

from functools import lru_cache

import mysql.connector as conn

from fastapi import Depends

from utils.utils import get_config_filename, get_app_secrets_filename

from .models import Task
from .models import User

#Atividade

# Criar             ok
# Ler               ok
# Atualizar         ok
# Remover usuário.  ok

#• Modificar as tarefas para adicionar o usuário responsável pela tarefa.   OK

    
# replace_user 
    #Temos que checar o new username se ele ja existe no DB                 OK

# create_user
    #try except de qdo o username ja existir no db                          OK

#Arrumar erro do create_new_task quando USername não existe                 OK


class DBSession:
    def __init__(self, connection: conn.MySQLConnection):
        self.connection = connection


    def create_user(self, user: User):
        
        if self.__user_exists(user.username):
            raise ValueError()
        query = "INSERT INTO users (username) VALUES (%s)"
        value = user.username
        with self.connection.cursor() as cursor:
            cursor.execute(query, (value,))
        self.connection.commit()

        #fazer o try e except para quando o usuario ja existir no DB
        return {"username" : user.username}

    def read_users(self):
        query = 'SELECT * FROM users'
 
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            db_results = cursor.fetchall()

        return {username[0]  for username in db_results}


    def replace_user(self, old, user: User):
        
        #Temos que checar tanto mo old username e o novo para ver se ele ja existe no DB
        if not self.__user_exists(old):
            raise KeyError()
        if self.__user_exists(user.username):
            raise ValueError()
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''
                UPDATE users SET username=%s
                WHERE username=(%s)
                ''',
                (user.username , old),
            )
        self.connection.commit()


    def remove_user(self, username):
        if not self.__user_exists(username):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                'DELETE FROM users WHERE username=(%s)',
                (username, ),
            )
        self.connection.commit()



    def remove_all_users(self):

        with self.connection.cursor() as cursor:
            cursor.execute('DELETE FROM users')
        self.connection.commit()


        

    def read_all_tasks(self, completed: bool = None):
        query = 'SELECT BIN_TO_UUID(uuid), description, completed, username FROM tasks'
        if completed is not None:
            query += ' WHERE completed = '
            if completed:
                query += 'True'
            else:
                query += 'False'

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            db_results = cursor.fetchall()

        return {
            uuid_: Task(
                username=field_username,
                description=field_description,
                completed=bool(field_completed),
            )
            for uuid_, field_description, field_completed, field_username in db_results
        }

    def read_user_tasks(self,username : str, completed: bool = None):
        
        if not self.__user_exists(username):
            raise KeyError()

        query = '''SELECT BIN_TO_UUID(uuid), description, completed, username FROM tasks 
                    WHERE username = %s'''
        if completed is not None:
            query += ' AND completed = '
            if completed:
                query += 'True'
            else:
                query += 'False'

        with self.connection.cursor() as cursor:
            cursor.execute(query, (username,))

            db_results = cursor.fetchall()

        return {
            uuid_: Task(
                username=field_username,
                description=field_description,
                completed=bool(field_completed),
            )
            for uuid_, field_description, field_completed, field_username  in db_results
        }

    def create_user_task(self, item: Task):
        uuid_ = uuid.uuid4()
        
        if not self.__user_exists(item.username):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO tasks VALUES (UUID_TO_BIN(%s), %s, %s, %s)',
                (str(uuid_), item.description, item.completed, item.username),
            )
        self.connection.commit()

        return uuid_

    def read_task(self, uuid_: uuid.UUID):
        if not self.__task_exists(uuid_):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT description, completed, username
                FROM tasks
                WHERE uuid = UUID_TO_BIN(%s)
                ''',
                (str(uuid_), ),
            )
            result = cursor.fetchone()

        return Task(description=result[0], completed=bool(result[1]), username=result[2])

    def replace_task(self, uuid_, item):
        if not self.__task_exists(uuid_):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                '''
                UPDATE tasks SET description=%s, completed=%s
                WHERE uuid=UUID_TO_BIN(%s)
                ''',
                (item.description, item.completed, str(uuid_)),
            )
        self.connection.commit()

    def remove_task(self, uuid_):
        if not self.__task_exists(uuid_):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                'DELETE FROM tasks WHERE uuid=UUID_TO_BIN(%s)',
                (str(uuid_), ),
            )
        self.connection.commit()

    def remove_all_tasks(self):
        with self.connection.cursor() as cursor:
            cursor.execute('DELETE FROM tasks')
        self.connection.commit()
    

    def remove_user_tasks(self, username):
        if not self.__user_exists(username):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                'DELETE FROM tasks WHERE username=%s',
                (username, ),
                )
            
        self.connection.commit()


    def __task_exists(self, uuid_: uuid.UUID):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT EXISTS(
                    SELECT 1 FROM tasks WHERE uuid=UUID_TO_BIN(%s)
                )
                ''',
                (str(uuid_), ),
            )
            results = cursor.fetchone()
            found = bool(results[0])

        return found

    def __user_exists(self, user: str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT EXISTS(
                    SELECT 1 FROM users WHERE username=(%s)
                )
                ''',
                (user, ),
            )
            results = cursor.fetchone()
            found = bool(results[0])

        return found


@lru_cache
def get_credentials(
        config_file_name: str = Depends(get_config_filename),
        secrets_file_name: str = Depends(get_app_secrets_filename),
):
    with open(config_file_name, 'r') as file:
        config = json.load(file)
    with open(secrets_file_name, 'r') as file:
        secrets = json.load(file)
    return {
        'user': secrets['user'],
        'password': secrets['password'],
        'host': config['db_host'],
        'database': config['database'],
    }


def get_db(credentials: dict = Depends(get_credentials)):
    try:
        connection = conn.connect(**credentials)
        yield DBSession(connection)
    finally:
        connection.close()
