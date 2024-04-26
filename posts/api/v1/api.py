'''
This module contains the API endpoints for the posts application. The API endpoints are used to interact with the application using HTTP requests. The API endpoints are used to retrieve and create posts and users
'''

from flask import jsonify, request

from posts import app, bcrypt, db, api_view
from posts.models import Post, User
from posts.api.v1.models import (
    users_schema, 
    user_schema, 
    post_schema, 
    posts_schema
)


@api_view.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        return users_schema.dump(users)
    if request.method == 'POST':
        try:
            res = request.json
            username_exists = User.query.filter_by(username=res.get('username')).first()
            email_exists = User.query.filter_by(username=res.get('email')).first()
            
            if username_exists:
                return jsonify({'message': 'This username is taken, please try another one', 'status': 500})
            if email_exists:
                return jsonify({'message': 'An account with this message already exists, please try signing in instead', 'status': 500})
            
            hashed_password = bcrypt.generate_password_hash(res.get('password')).decode('utf-8')
            user = User(username=res.get('username'), 
                        email=res.get('email'), 
                        password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'Account created successfully', 'status': 201})
        except:
            return jsonify({'message': 'Account could not be created by this time.', 'status': 500})


@api_view.route('/users/<int:id>', methods=['GET', 'POST'])
def user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found', 'status': 404})
    return user_schema.dump(user)


@api_view.route('/posts', methods=['GET', 'POST'])
def posts():
    posts = Post.query.all()
    return posts_schema.dump(posts)


@api_view.route('/posts/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    if not post:
        return jsonify({'message': 'Post not found', 'status': 404})
    return post_schema.dump(post)


@api_view.route('/search', methods=['GET', 'POST'])
def search():
    search_query = request.json.get('q')
    posts = Post.query.filter(Post.title.like(f'%{search_query}%')).all()
    return posts_schema.dump(posts)
