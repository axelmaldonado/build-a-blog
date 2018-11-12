from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Maldonado@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(400))
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.deleted = False

@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def create_blog():

    id_check = request.args.get("id")
    if id_check is not None:
        post_id = int(request.args.get("id"))
        post = Blog.query.filter_by(id=post_id).first()
        return render_template("single-blog.html", post=post)
    else:
        posts = Blog.query.filter_by(deleted=False).all()

    return render_template("index.html", posts=posts)

@app.route('/blog/newpost', methods=['GET', 'POST'])
def new_post():
    
    if request.method == "POST":
        blog_title = request.form['blog-title']
        blog_post = request.form['blog-post']
        title_error = ""
        post_error = ""

        if blog_title == "":
            title_error = "Enter a Blog title for your post"
        if len(blog_title) > 50:
            title_error = "Blog title limit is 120 characters"
        if blog_post == "":
            post_error = "Please enter a Blog post before submitting"
        if len(blog_post) > 300:
            post_error = "Please limit your Blog post to 400 characters"

        if not title_error and not post_error:
            new_post = Blog(blog_title, blog_post)
            db.session.add(new_post)
            db.session.commit()
            post_id = (new_post.id)
            return redirect(url_for("create_blog", id=post_id))
        else:
            return render_template("add-blog.html",title_error=title_error, post_error=post_error)

    return render_template('add-blog.html')

if __name__ == '__main__':
    app.run()