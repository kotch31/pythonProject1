from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK _MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    category = db.Column(db.String(100))
    note = db.Column(db.String(1000))


@app.route('/')
def index():
    # show all todos
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    category = request.form.get("category")
    note = request.form.get("note")
    new_todo = Todo(title=title, category=category, note=note, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

def search_cat(category):
    #search by title
    search_category = request.form.get("search")
    if search_category:
        search_results = Todo.query.filter(db.or_(Todo.category.ilike(f"%{search_term}%")))
    else:
        search_results = Todo.query.all()




@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
