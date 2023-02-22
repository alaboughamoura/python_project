from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.serial_medical = data['serial_medical']
        self.password = data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
    
    @classmethod 
    def register(cls, data):
        query = """
                INSERT INTO doctors (first_name, last_name, email,serial_medical,password) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s,%(serial_medical)s, %(password)s)
                """
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM doctors WHERE email = %(email)s"
        result= connectToMySQL(DB).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    @classmethod
    def get_serial_number(cls, data):
        query = "SELECT * FROM doctors WHERE serial_medical = %(serial_medical)s"
        result= connectToMySQL(DB).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    @classmethod
    def get_by_id(cls, data): #!READ
        query="SELECT * FROM doctors WHERE id=%(id)s;"
        result= connectToMySQL(DB).query_db(query,data)
        print(result)
        if len(result) <1:
            return False
        return cls(result[0])
    # validation
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name'])<4:
            is_valid = False
            flash("Invalid first name, must be greater than 3 characters!", "first_name")
        if len(data['last_name'])<4:
            is_valid = False
            flash("Invalid last name, must be greater than 3 characters!", "last_name")



            #   add the serial number 
            
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", "email")
            is_valid = False
        elif User.get_by_email({'email': data['email']}):
            is_valid = False
            flash("email address already exists!", "email")
        if len(data['password'])<4:
            is_valid = False
            flash("Invalid password, must be greater than 8 characters!", "password")
        elif data['password']!=data['confirm_password']:
            flash("Passwords don't match", "confirm_password")
            is_valid = False
        return is_valid