from flask import Flask , render_template ,request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model) : 
    slno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(200) , nullable = False)
    desc = db.Column(db.String(500) , nullable = False)
    date_create = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.slno} - {self.title}"
    
with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/index" , methods=['GET' , 'POST'])
def indexx():
    if request.method == 'POST' : 
        # print(request.form.get('title')) 
        title = request.form.get('title')
        desc = request.form.get('desc')

        todo = Todo(title=title , desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    # print(alltodo)
    return render_template("index.html" , altodo = alltodo)

@app.route("/show")
def show():
    alltodo = Todo.query.all()
    print(alltodo)
    return "<p>Hello, World 2!</p>"

@app.route("/update/<int:slno>" , methods=['GET' , 'POST'])
def update(slno):
    if request.method == 'POST' : 
        # print(request.form.get('title')) 
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = Todo.query.filter_by(slno = slno).first()
        todo.title = title
        todo.desc = desc
        # todo = Todo(title=title , desc=desc)
        db.session.add(todo)
        db.session.commit()

        return redirect('/index')
    todo = Todo.query.filter_by(slno = slno).first() #pass it in html
    return render_template('update.html' , todo = todo)

@app.route("/delete/<int:slno>")
def delete(slno):
    todo = Todo.query.filter_by(slno = slno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/index')

if __name__ == '__main__' : 
    app.run(debug=True , port=8000)