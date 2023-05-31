from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__) # __name__ is a special variable in python that is just the name of the module

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#change this above line if you want to use a different database
db = SQLAlchemy(app)    # initialize the database
#when you update database run the following commands in the terminal
# from app import app, db
# app.app_context().push()
# db.create_all()

class Todo(db.Model):   # create a model for the database
    id = db.Column(db.Integer, primary_key=True) # primary_key=True means it's unique
    completed = db.Column(db.Integer, default=0) # default=0 means it's not completed (0 is false)
    content = db.Column(db.String(200), nullable=False) # nullable=False means it can't be empty
    date_created = db.Column(db.DateTime, default=datetime.utcnow) # default=datetime.utcnow means it will use the current time
    due_date = db.Column(db.DateTime, nullable=False) # nullable=True means it can be empty
    priority = db.Column(db.String(10), nullable=True) # nullable=True means it can be empty
    def __repr__(self): # this is what will be shown when we query the database
        return '<Task %r>' % self.id # this will return the id of the task

@app.route('/', methods = ['POST', 'GET']) # this is a decorator, it tells the app what url to trigger the function
def index(): 
    if request.method == 'POST':    # if the request is a POST request
        task_content = request.form['content']
        
        task_due_date_str = request.form['due_date']

        task_priority = request.form['priority']

        task_due_date = datetime.strptime(task_due_date_str, '%Y-%m-%d')

        new_task = Todo(content=task_content, due_date=task_due_date, priority=task_priority) # create a new task
        try:
            db.session.add(new_task)    # add the new task to the database
            db.session.commit()         # commit the changes
            return redirect('/')        # redirect to the index page
        except Exception as e:
            print(str(e))  # print the error message to the console for debugging purposes
            return 'There was an issue adding your task'
    else :
        tasks = Todo.query.order_by(Todo.date_created).all() # get all the tasks from the database
        return render_template('index.html', tasks = tasks) # render the index.html template and pass in the tasks

@app.route('/delete/<int:id>') # this is a decorator, it tells the app what url to trigger the function
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete) # delete the task
        db.session.commit()               # commit the changes
        return redirect('/')              # redirect to the index page
    except Exception as e:
        print(str(e))
        return 'There was a problem deleting that task'
    
@app.route('/update/<int:id>', methods=['GET', 'POST']) # this is a decorator, it tells the app what url to trigger the function
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':    # if the request is a POST request
        task.content = request.form['content']
        task_due_date_str = request.form['due_date']

        task.priority = request.form['priority']

        task_due_date = datetime.strptime(task_due_date_str, '%Y-%m-%d')
        task.due_date = task_due_date

        try:
            db.session.commit()         # commit the changes
            return redirect('/')        # redirect to the index page
        except Exception as e:
            print(str(e))
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)
    
if __name__ == "__main__":  # this is to make sure that the app only runs when we run this file directly
    app.run(debug=True)     # debug=True means that we don't have to restart the server every time we make a change

 