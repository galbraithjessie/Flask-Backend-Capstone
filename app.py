from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
import os


app = Flask(__name__)
heroku = Heroku(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.String(255), unique=False)

    def __init__(self, title, content, id):
        self.title = title
        self.content = content
        self.id = id

class BlogSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content', 'id')


blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)

# Endpoint to create a new blog
@app.route('/blog', methods=["POST"])
def add_blog():
    title = request.json['title']
    content = request.json['content']

    new_blog = Blog(title, content)

    db.session.add(new_blog)
    db.session.commit()

    blog = Blog.query.get(new_blog.id)

    return blog_schema.jsonify(blog)


# Endpoint to query all blogs
@app.route("/blogs", methods=["GET"])
def get_blogs():
    all_blogs = Blog.query.all()
    result = blogs_schema.dump(all_blogs)
    return jsonify(result)


# Endpoint for querying a single blog
@app.route("/blog/<id>", methods=["GET"])
def get_blog(id):
    blog = Blog.query.get(id)
    return blog_schema.jsonify(blog)


# Endpoint for updating a blog
@app.route("/blog/<id>", methods=["PUT"])
def blog_update(id):
    blog = Blog.query.get(id)
    title = request.json['title']
    content = request.json['content']

    blog.title = title
    blog.content = content

    db.session.commit()
    return blog_schema.jsonify(blog)


# Endpoint for deleting a record
@app.route("/blog/<id>", methods=["DELETE"])
def blog_delete(id):
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()

    return "Blog was successfully deleted"


if __name__ == '__main__':
    app.run(debug=True)