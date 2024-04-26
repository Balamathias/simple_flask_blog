import os
import secrets
from flask import flash, json, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image

from posts import bcrypt
from posts import app, db, login_manager
from posts.decorators import is_authenticated
from posts.form import LoginForm, PostForm, RegisterForm, UpdateAccountForm
from posts.models import Post, User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_dict_for_all_templates():
    profile_picture = 'static/profile_pics/default.jpg'
    if current_user.is_authenticated:
        profile_picture = url_for('static', filename='profile_pics/' + current_user.picture)
    return dict(profile_picture=profile_picture)


@app.route('/')
def home():
    posts = Post.query.all()
    sorted_posts = sorted(posts, key=lambda x: x.date_posted, reverse=True)
    return render_template('home.html', data='Hello HBNB!', posts=sorted_posts)


@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post, title=post.title)


@app.route('/register', methods=['GET', 'POST'])
@app.route('/sign-up', methods=['GET', 'POST'])
def register():
    if (current_user.is_authenticated):
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} successfully!', 'green')
        return redirect(url_for('home'))
    return render_template('register.html', form=form, title="Register | Sign Up")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if (current_user.is_authenticated):
        return redirect(url_for('home'))
    form = LoginForm()
    next_url = request.args.get('next')
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=form.remember_me.data)
        flash(f'Signed In successfully.', 'green')
        return redirect(next_url) if next_url else  redirect(url_for('home'))
    return render_template('login.html', form=form, title="Login")


@app.route('/logout')
def logout():
    logout_user()
    flash(f'Signed Out successfully.', 'green')
    return redirect(url_for('home'))


def save_picture(picture):
    random_hex = secrets.token_hex(12)
    _, f_ext = os.path.splitext(picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_name)
    dimensions = (200, 200)
    i = Image.open(picture)
    i.thumbnail(dimensions)
    i.save(picture_path)
    return picture_name


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.picture = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account updated successfully!', 'green')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_picture = url_for('static', filename='profile_pics/' + current_user.picture)
    return render_template('account.html', title="Account", form=form, profile_picture=profile_picture)


@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Posted successfully", 'green')
        return redirect(url_for('home'))
    return render_template('create-post.html', form=form, title="New post")


@app.route('/posts/<int:post_id>/update', methods=['PUT', 'GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Post updated successfully", 'green')
        return redirect(url_for('home'))
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    form.action = 'Update'
    return render_template('update_post.html', form=form, title=f"{post.title} | Update")


@app.route('/search', methods=['GET', 'POST'])
def search():
    search = request.args.get('q')
    posts = Post.query.filter(Post.title.contains(search) | Post.content.contains(search)).all()
    return render_template('search.html', posts=posts, search=search)


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Password reset instructions sent to {form.email.data} successfully!', 'green')
        return redirect(url_for('home'))
    return json.jsonify({'message': 'Forgot Password'})
