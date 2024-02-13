from flask import Flask, render_template, request, redirect, url_for
# imports flask
from flask_sqlalchemy import SQLAlchemy
# imports sql alchemy add on

app = Flask(__name__)
# name of app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# sets configuration for database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    # creates class for database
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    category = db.Column(db.String(100))
    due = db.Column(db.String(10))
    note = db.Column(db.String(1000))



@app.route('/')
def index():
    # show all todos
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    # add new to do
    title = request.form.get("title")
    category = request.form.get("category")
    note = request.form.get("note")
    due = request.form.get("due")
    # gets something from the input function and puts on the new to do
    new_todo = Todo(title=title, category=category, note=note, due=due, complete=False)
    # inputs new to do into database
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # updates completion status by id
    todo = Todo.query.filter_by(id=todo_id).first()
    # filters using the id given to each individual to do
    todo.complete = not todo.complete
    db.session.commit()
    # saves updated completion status to database
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # deletes item identified by id
    todo = Todo.query.filter_by(id=todo_id).first()
    # filters by id and removes from database
    db.session.delete(todo)
    db.session.commit()
    # removes data and saves data base
    return redirect(url_for("index"))

@app.route("/searchcat", methods=["GET", "POST"])
def search_cat():
    # search by category
    search_category = request.args.get("search_cat")
    if search_category:
        search_results = Todo.query.filter(Todo.category.ilike(f"%{search_category}%"))
    else:
        search_results = Todo.query.all()
    return render_template('base.html', todo_list=search_results)

@app.route("/searchdue", methods=["GET", "POST"])
def search_due():
    #search by due date
    search_date = request.args.get("search_date")
    if search_date:
        search_results = Todo.query.filter(Todo.due.ilike(f"%{search_date}%"))
    else:
        search_results = Todo.query.all()
    return render_template('base.html', todo_list=search_results)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
# creates app database
    app.run(debug=True)
# tells it to "go"