#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'komorebi'


from flask import render_template, redirect, url_for, flash, request, g, abort
from flask_login import login_user, current_user, logout_user
from forms import CreatePostForm, UserForm, LoginForm, CommentForm
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login_manager
from models import BlogPost, User, Comment
from functools import wraps


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = UserForm()
    if request.method == "POST" and form.validate_on_submit():
        if check_email(form.email.data):
            flash('The email is existed')
            return render_template('register.html', form=form)
        else:
            user = User()
            user.name = form.name.data
            user.email = form.email.data
            user.password = generate_password_hash(
                password=form.password.data,
                method='pbkdf2:sha256',
                salt_length=8)
            db.session.add(user)
            try:
                db.session.commit()
                login_user(user)
                return redirect(url_for('get_all_posts'))
            except Exception:
                db.session.rollback()
    return render_template("register.html", form=form)


def check_email(email):
    result = User.query.filter_by(email=email).first()
    return True if result else False


def admin_only(fn):
    @wraps(fn)  # @wraps can still keep fn's attributes like __name__,__doc__
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.id != 1:  # id=1 means admin, only admin can do some operations
            # Raise an HTTPException for the given status code.
            return abort(403)
        return fn(*args, **kwargs)
    return wrapper


@login_manager.user_loader
def user_loader(user_id):
    user = User.query.get(user_id)
    return user if user else None


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        if check_email(form.email.data):
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('get_all_posts'))
            else:
                flash("Incorrect Password")
                return render_template("login.html", form=form)
        else:
            flash('The email does not exist.')
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)
    if request.method == "POST" and form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment()
            comment.body = form.body.data
            comment.time = date.today().strftime("%B %d, %Y")
            comment.user_id = current_user.id
            comment.author = current_user
            comment.post_id = post_id
            db.session.add(comment)
            try:
                db.session.commit()
                return render_template(
                    "post.html",
                    post=requested_post,
                    form=form)
            except Exception:
                db.session.rollback()
        else:
            flash("You need to login or register to comment.")
            return render_template(
                "post.html",
                post=requested_post,
                form=form)
    return render_template(
        "post.html",
        post=requested_post,
        form=form)


@ app.route("/about")
def about():
    return render_template("about.html")


@ app.route("/contact")
def contact():
    return render_template("contact.html")


@ app.route("/new-post", methods=["GET", "POST"])
@ admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y"),
            user_id=current_user.id
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@ app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@ admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        obj=post
    )
    if request.method == "POST" and edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form)


@ app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))



