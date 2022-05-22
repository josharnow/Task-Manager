from flask import flash
from flask_app import app
import re

from flask_app.config.mysqlconnection import connectToMySQL

class User:
  """The User data model
  """  
  def __init__(self, data): # "data" represents data from the database
    """Constructor function

    Args:
        data (list of dict of {str : int, str : str, str : str, str : str, datetime.datetime, datetime.datetime): Data retrieved from the database
    """    
    
    self.id = data['id']
    self.username = data['username']
    self.email = data['email']
    self.password = data['password']
    self.created_at = data['created_at']
    self.updated_at= data['updated_at']
    
  @classmethod
  def create_user(cls, data):
    """Creates a user in the mySQL database

    Args:
        data (dict of {str : str}): Data passed in from register_user() in login.py

    Returns:
        int or bool: The ID number of the row inserted, or an error
    """
    
    query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
    
    result = connectToMySQL('task_manager').query_db(query, data)
    
    return result
  
  @classmethod
  def get_users_with_email(cls, data):
    """Finds users in the database with a given email

    Args:
        data (dict of {str : str}): Data passed in from validate_registration(data) in user.py

    Returns:
        list of list of dict of {str : int, str : str, str : str, str : str, datetime.datetime, datetime.datetime} or list of bool: Users found with the given email in the mySQL database, or an error
    """    
    
    query = "SELECT * FROM users WHERE email = %(email)s;"
    
    results = connectToMySQL('task_manager').query_db(query, data)
    
    users = []

    for item in results:
      users.append(User(item))
    
    return users
  
  @classmethod
  def get_users_with_username(cls, data):
    """Finds users in the database with a given username

    Args:
        data (str or dict of {str : str}): Data passed in from login_user() in login.py or validate_registration(data) in user.py

    Returns:
        list of list of dict of {str : int, str : str, str : str, str : str, datetime.datetime, datetime.datetime} or list of bool: Users found with the given username in the mySQL database, or an error
    """    
    
    query = "SELECT * FROM users WHERE username = %(username)s;"
    
    results = connectToMySQL('task_manager').query_db(query, data)
    
    print(results)
    
    users = []

    for item in results:
      users.append(User(item))
    
    return users
  
  @staticmethod
  def validate_registration(data):
    """Validates user registration

    Args:
        data (dict of {str : str}): Data passed in from register_user() in login.py

    Returns:
        bool: Defines if registration is valid
    """    
    
    is_valid = True
    email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
    
    # Username between 2 and 32 characters
    if len(data['username']) < 2 or len(data['username']) > 32:
      flash("Username should be 2 to 32 characters.")
      is_valid = False
      
      
    # Email address should be valid
    if not email_regex.match(data['email']):
      flash("Please provide a valid email address.")
      is_valid = False
    
    # Password should be at least 8 characters
    if len(data['password']) < 8:
      flash("Please use a password of at least eight characters.")
      is_valid = False
    
    # Password and confirm password should match
    if data['password'] != data['confirm_password']:
      flash("Please ensure password and confirm password match.")
      is_valid = False
    
    # Ensure email address is not in use
    if len(User.get_users_with_email({'email': data['email']})) != 0:
      flash("This email address is already in use.")
      is_valid = False
      
    # Ensure username is not in use
    if len(User.get_users_with_username({'username': data['username']})) != 0:
      flash("This username is already in use.")
      is_valid = False
    
    return is_valid