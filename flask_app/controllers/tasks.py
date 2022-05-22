from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.task import Task
import datetime

@app.route('/dashboard')
def dashboard():
  if 'user_id' not in session:
    flash('Please log in to view this page.')
    return redirect('/')
  
  data = {
    'user_id': session['user_id']
  }
  
  tasks = Task.get_all_tasks()
  
  return render_template('dashboard.html', tasks=tasks)

@app.route('/tasks/new')
def new_task():
  return render_template('new_task.html')

@app.route('/tasks/create', methods=['POST'])
def add_task():
  if Task.validate_task(request.form):
    # Create task here
    data = {
        'task_name': request.form['task_name'],
        'due_date': request.form['due_date'],
        'privacy_status': request.form['privacy_status'],
        'completion_status': request.form['completion_status'],
        'description': request.form['description'],
        # user_id is stored in session by login_user() in login.py
        'user_id': session['user_id']
    }

    Task.add_task(data)

    print('Task is valid')
    return redirect('/dashboard')

  print('Task is invalid')
  return redirect('/tasks/new')

@app.route('/tasks/<int:task_id>')
def task_info(task_id):
  task = Task.get_task_by_id({'id': task_id})

  if session['user_id'] != task.user.id and task.privacy_status == 0:
    flash(f'Please log in as the appropriate user to view this page (Task ID #{task.id}).')
    return redirect('/dashboard')

  return render_template('task_info.html', task=task)

@app.route('/tasks/<int:task_id>/edit')
def edit_task(task_id):
  task = Task.get_task_by_id({'id': task_id})

  if session['user_id'] != task.user.id:
    flash(f'Please log in as the appropriate user to view this page (Task ID #{task.id}).')
    return redirect('/dashboard')

  return render_template('edit_task.html', task=task)

@app.route('/tasks/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
  task = Task.get_task_by_id({'id': task_id})

  if session['user_id'] != task.user.id:
    flash(f'Please log in as the appropriate user to view this page (Task ID #{task.id}).')
    return redirect('/dashboard')

  if Task.validate_task(request.form):
    if request.form['completion_status'] == "0":
      data = {
          'task_name': request.form['task_name'],
          'description': request.form['description'],
          'due_date': request.form['due_date'],
          'privacy_status': request.form['privacy_status'],
          'completion_status': request.form['completion_status'],
          'completion_date': None,
          'id': task_id
      }

      Task.update_task(data)
      return redirect(f'/tasks/{task_id}')
    
    if request.form['completion_status'] == "1" and task.completion_status == 0:
      data = {
          'task_name': request.form['task_name'],
          'description': request.form['description'],
          'due_date': request.form['due_date'],
          'privacy_status': request.form['privacy_status'],
          'completion_status': request.form['completion_status'],
          'completion_date': datetime.datetime.now(),
          'id': task_id
      }

      Task.update_task(data)
      return redirect(f'/tasks/{task_id}')
    

  return redirect(f'/tasks/{task_id}/edit')

@app.route('/tasks/<int:task_id>/update_completion_status', methods=['POST'])
def update_task_completion_status(task_id):
  task = Task.get_task_by_id({'id': task_id})

  if session['user_id'] != task.user.id and task.privacy_status == 0:
    flash(f'Please log in as the appropriate user to view this page (Task ID #{task.id}).')
    return redirect('/dashboard')

  if Task.validate_task(request.form):
    if request.form['completion_status'] == "0":
      data = {
          'task_name': request.form['task_name'],
          'description': request.form['description'],
          'due_date': request.form['due_date'],
          'privacy_status': request.form['privacy_status'],
          'completion_status': request.form['completion_status'],
          'completion_date': None,
          'id': task_id
      }

      Task.update_task(data)
      return redirect(f'/dashboard')

    if request.form['completion_status'] == "1" and task.completion_status == 0:
      data = {
          'task_name': request.form['task_name'],
          'description': request.form['description'],
          'due_date': request.form['due_date'],
          'privacy_status': request.form['privacy_status'],
          'completion_status': request.form['completion_status'],
          'completion_date': datetime.datetime.now(),
          'id': task_id
      }

      Task.update_task(data)
      return redirect(f'/dashboard')

  return redirect(f'/dashboard')

@app.route('/tasks/<int:task_id>/delete')
def delete_task(task_id):
  task = Task.get_task_by_id({'id': task_id})

  if session['user_id'] != task.user.id:
    flash(f'Please log in as the appropriate user to view this page (Task ID #{task.id}).')
    return redirect('/dashboard')

  return render_template('delete_task.html', task=task)

@app.route('/tasks/<int:task_id>/confirm')
def confirm_delete_task(task_id):
  task = Task.get_task_by_id({'id': task_id})
  task.delete_task({'id': task_id})

  return redirect('/dashboard')
