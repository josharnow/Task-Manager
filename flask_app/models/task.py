from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
import datetime

class Task:
  def __init__(self, data):
    self.id = data['id']
    self.task_name = data['task_name']
    self.description = data['description']
    self.due_date = data['due_date']
    self.privacy_status = data['privacy_status']
    self.completion_status = data['completion_status']
    self.completion_date = data['completion_date']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.user_id = data['user_id']
    self.user = None
    # self.current_datetime = datetime.datetime.now()

  @classmethod
  def add_task(cls, data):
    query = "INSERT INTO tasks (task_name, description, due_date, privacy_status, completion_status, user_id) VALUES (%(task_name)s, %(description)s, %(due_date)s, %(privacy_status)s, %(completion_status)s, %(user_id)s);"

    result = connectToMySQL('tfc_test_project').query_db(query, data)

    return result

  @classmethod
  def get_all_tasks(cls):
    query = 'SELECT * FROM tasks JOIN users ON tasks.user_id = users.id;'

    results = connectToMySQL('tfc_test_project').query_db(query)

    tasks = []

    for item in results:
      task = cls(item)
      user_data = {
        'id': item['users.id'],
        'username': item['username'],
        'email': item['email'],
        'password': item['password'],
        'created_at': item['users.created_at'],
        'updated_at': item['users.updated_at']
      }
      task.user = User(user_data)
      tasks.append(task)

    return tasks

  @classmethod
  def get_all_tasks_from_user(cls, data):
    query = 'SELECT * FROM tasks WHERE tasks.user_id = %(user_id)s;'

    results = connectToMySQL('tfc_test_project').query_db(query, data)

    tasks = []

    for item in results:
      task = cls(item)
      user_data = {
        'id': item['users.id'],
        'username': item['username'],
        'email': item['email'],
        'password': item['password'],
        'created_at': item['users.created_at'],
        'updated_at': item['users.updated_at']
      }
      task.user = User(user_data)
      tasks.append(task)

    return tasks

  @classmethod
  def get_task_by_id(cls, data):
    query = "SELECT * FROM tasks JOIN users ON tasks.user_id = users.id WHERE tasks.id = %(id)s;"

    result = connectToMySQL('tfc_test_project').query_db(query, data)

    task = cls(result[0])
    user_data = {
      'id': result[0]['users.id'],
      'username': result[0]['username'],
      'email': result[0]['email'],
      'password': result[0]['password'],
      'created_at': result[0]['users.created_at'],
      'updated_at': result[0]['users.updated_at']
    }
    task.user = User(user_data)

    return task

  @classmethod
  def update_task(cls, data):
    query = 'UPDATE tasks SET task_name = %(task_name)s, description = %(description)s, due_date = %(due_date)s , privacy_status = %(privacy_status)s, completion_status = %(completion_status)s, completion_date = %(completion_date)s WHERE id = %(id)s;'

    connectToMySQL('tfc_test_project').query_db(query, data)

  @classmethod
  def delete_task(cls, data):
    query = 'DELETE FROM tasks WHERE id = %(id)s;'

    connectToMySQL('tfc_test_project').query_db(query, data)

  @staticmethod
  def validate_task(data):
    is_valid = True

    if len(data['task_name']) < 1 or len(data['task_name']) > 60:
      flash("The task name should be between 1 and 60 characters.")
      is_valid = False

    if len(data['description']) > 1000:
      flash("The description should be less than 1,000 characters.")
      is_valid = False
      
    if len(data['due_date']) < 1:
      flash("A due date must be set.")
      is_valid = False

    return is_valid
