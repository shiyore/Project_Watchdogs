#test program 1 from video
from datetime import datetime
from flask import Flask, render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

all_posts = [
    {
        'title': 'post1',
        'author': 'John Doe',
        'content': "this is the content of post1"
    },
    {
        'title': 'post2',
        'content': "this is the content of post2"
    }
]
#both of these lead to hello()
#the route leads to the closest linear function in the program
@app.route("/")
@app.route("/home")
def home():
    #using templates
    return render_template('index.html')


#passing data to html
#use dictionaries to make it easier with jinja on the html page
@app.route("/posts", methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author='Aiden')
        db.session.add(new_post)
        try:
            db.session.commit()
            db.session.remove()
        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            print(str(e))
            db.session.rollback()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        db.session.close()
        return render_template('posts.html', posts=all_posts)

#how to pass variables using url
#specify the data type within the <> befor  the colon ex. <int:id> <string:name>
@app.route("/hello/<string:name>")
def hell(name):
    return "Hello, " + name

@app.route("/image/<string:url>")
def display_image(url):
    return "<img src=" + url + " >"


#specifying web methods. You can have multiple requests as well
@app.route('/getonly', methods=['GET'])
def get_req():
    return 'You can only get this webpage'


if __name__ == "__main__":
    app.run(debug=True)
    
