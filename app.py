
# importing required packages
from flask import Flask , render_template , session , request , redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

# initializing the app 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# backend fetching  .. for data fetching
class Todo(db.Model):
      
      '''creating table using sqlite'''
      sno = db.Column(db.Integer , primary_key = True)
      title = db.Column(db.String(200) , nullable = False)
      desc = db.Column(db.String(500) , nullable = False)
      date_created = db.Column(db.DateTime , default = datetime.utcnow)
      
      '''to print the result when called the class'''
      def __repr__(self) -> str:
            return f"{self.sno} - {self.title}"

# home page
@app.route('/', methods = ['GET' , 'POST'])
def home():
      
      # to get the requests or data from the form
      if request.method == 'POST':
            title = request.form['title']
            desc = request.form['desc']
            todo = Todo(title = title, desc = desc)
            db.session.add(todo)
            db.session.commit()
      
      # to get the all the queries
      allTodo = Todo.query.all()
      return render_template('index.html', allTodo = allTodo)

@app.route('/show')
def show():
      allTodo = Todo.query.all()
      print(allTodo)
      

@app.route('/update<int:sno>', methods = ['GET' , 'POST'])
def update(sno):
      if request.method == 'POST':
            title = request.form['title']
            desc = request.form['desc']
            todo = Todo.query.filter_by(sno = sno).first()
            todo.title = title
            todo.desc = desc
            db.session.add(todo)
            db.session.commit()
            return redirect('/')
      
      todo = Todo.query.filter_by(sno = sno).first()
      return render_template('update.html', todo = todo)


@app.route('/delete<int:sno>')
def delete(sno):
      todo = Todo.query.filter_by(sno = sno).first()
      db.session.delete(todo)
      db.session.commit()
      return redirect('/')
      
# we can change the port also and can assign to 8000


'''
"debug = True" only when we are in developer stage to see the error's if there are any.
after done setting it and publishing it , we have to set it False. 
'''
if __name__ == '__main__':
      app.run(debug=True)