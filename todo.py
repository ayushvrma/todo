import datetime
from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine("postgres://postgres:1234@localhost:5432/todo")
db = scoped_session(sessionmaker(bind=engine))

@app.route('/', methods=['GET','POST'])
def index():
    redirect("index.html")
    tasks=db.execute("SELECT * FROM todo").fetchall()
    if request.method == "POST":
        task=request.form.get("task")
        d=datetime.date.today()
        db.execute("INSERT INTO todo (task,date) VALUES(:task,:date)",{"task":task,"date":d})
        db.commit()

    return render_template("index.html",tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    if db.execute("SELECT * FROM todo WHERE id=:id",{"id":id}).rowcount == 0:
        return render_template("error.html", message="no task as such exists")
    db.execute("DELETE FROM todo WHERE id=:id",{"id":id})
    db.commit()
    return redirect("/")

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    if db.execute("SELECT * FROM todo WHERE id=:id",{"id":id}).rowcout == 0:
        return render_template(error.html, message="no task as such exists")
    ntask=request.form.get("ntask")
    nd=datetime.date.today()
    db.execute("UPDATE todo SET task=:task, date=:date WHERE id=:id",{"task":ntask,"id":id,"date":nd})
    db.commit()
    return render_template("update.html")
