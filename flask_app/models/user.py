from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt  
from flask import flash      
import re
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,db_data):
        self.id = db_data['id']
        self.first_name= db_data['first_name']
        self.last_name= db_data['last_name']
        self.email= db_data['email']
        self.password= db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.notes = []


    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        item_from_db = connectToMySQL('notes_app').query_db(query,data)
        return cls(item_from_db[0])


    @classmethod
    def login(cls,data):
        query = """SELECT * FROM users WHERE email = %(email)s;
                """
        result = connectToMySQL('notes_app').query_db(query,data)
        
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod
    def save( cls ,data ):
        query = """INSERT INTO users ( first_name , last_name , email , password , created_at , updated_at ) 
        VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s , NOW() , NOW());"""
        return connectToMySQL('notes_app').query_db(query,data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        # test pattern 
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid eamil address!")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_registration(user):
        print("user_validated")
        is_valid = True
        if len(user['first_name']) < 1:
            flash("Firstname required")
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Lastname required")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid eamil address!")
            is_valid = False
        if len(user['password']) < 6:
            flash("Password must be atleast 6 characters")
            is_valid = False
        return is_valid