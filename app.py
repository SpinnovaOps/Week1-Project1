from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks")
def view_tasks():
    tasks = Task.query.all()
    return render_template("tasks.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task_text = request.form.get("task")
    if task_text:
        new_task = Task(task=task_text)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for("view_tasks"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("view_tasks"))

@app.route("/recent-added")
def show_recent_added():
    last_task = Task.query.order_by(Task.id.desc()).first()
    return render_template("recent_added.html", task=last_task.task if last_task else None)

@app.route("/recent-deleted")
def show_recent_deleted():
    # Note: To track deleted tasks, we'd need another table or logging system
    return render_template("recent_deleted.html", task="Tracking deleted tasks requires a log.")

if __name__ == "__main__":
    app.run(debug=True)
