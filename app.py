from flask import Flask, render_template, redirect, url_for, request, flash
from extensions import db  # Import from extensions.py
from models import Task
from datetime import datetime
from forms import TaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db.init_app(app)  # Initialize the app with SQLAlchemy

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(title=form.title.data, description=form.description.data, due_date=form.due_date.data)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!')
        return redirect(url_for('index'))

    tasks = Task.query.all()
    return render_template('index.html', form=form, tasks=tasks)

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = True
    db.session.commit()
    flash('Task marked as completed!')
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!')
    return redirect(url_for('index'))

@app.route('/stats')
def stats():
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    return render_template('stats.html', total_tasks=total_tasks, completed_tasks=completed_tasks, pending_tasks=pending_tasks)

if __name__ == '__main__':
    app.run(debug=True)
