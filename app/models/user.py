from app.config.mysqlconnection import connectToMySQL
from flask import flash


import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db_name = 'top_25'

    def __init__(self, data):
        self.id = data['id']
        self.fullname = data['full_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #  Create one User
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (full_name, email, password, created_at, updated_at) VALUES ( %(full_name)s, %(email)s, %(password)s, CURRENT_TIMESTAMP, NOW());"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        print(result)
        return result

    # Get user by email
    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        user = User(result[0])
        return user

    # Get All Users

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    # Get one user

    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        user = User(result[0])
        return user

    @staticmethod
    def validate_user(user):
        is_valid = True

        name_regex = re.compile(r'^[a-zA-Z ]+$')

        if len(user['fullname']) < 3 or not name_regex.match(user['fullname']):
            flash('Name is not valid', 'register')
            is_valid = False

        if not email_regex.match(user['email']):
            flash('Invalid email address.', 'register')
            is_valid = False

        if len(user['password']) < 8:
            flash('Password should be at least 8 characters.', 'register')
            is_valid = False

        if user['password'] != user['conf_password']:
            flash('Passwords do not match.', 'register')
            is_valid = False

        return is_valid
