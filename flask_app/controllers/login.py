from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
  """Renders the login/registration page

  Returns:
      str: The result of evaluating index.html
  """  
  
  return render_template('index.html')


@app.route('/users/register', methods=['POST'])
def register_user():
  """Registers user

  Returns:
      requests.Response: The response dictionary (object)
  """  
  
  # Validate the form data
  if User.validate_registration(request.form):
    # Hash password here
    data = {
      'username': request.form['username'],
      'email': request.form['email'],
      'password': bcrypt.generate_password_hash(request.form['password'])
    }
    
    user_id = User.create_user(data)
    
    session['user_id'] = user_id
    
    return redirect('/dashboard')
  
  else:
    # Create user if data is valid
    return redirect('/')

@app.route('/users/login', methods=['POST'])
def login_user():
  """Logs user in

  Returns:
      requests.Response: The response object
  """  
  users = User.get_users_with_username(request.form)
  
  if len(users) != 1:
    flash('User with the given username does not exist.')
    return redirect('/')
  
  user = users[0]
  
  if not bcrypt.check_password_hash(user.password, request.form['password']):
    flash('Password for the given user is incorrect.')
    return redirect('/')
  
  session['user_id'] = user.id
  session['user_username'] = user.username
  
  return redirect('/dashboard')

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')