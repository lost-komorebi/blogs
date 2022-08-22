#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'komorebi'
from app import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship


# CONFIGURE TABLES

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)  # foreign key relates to user.id
    # backref can use post.comments to get all comments of that post
    comments = relationship("Comment", backref="post")
    author = relationship("User", backref="post")


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    email = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(50), nullable=True)
    # this column will not appear in the database
    posts = relationship("BlogPost", backref='user')
    # this column will not appear in the database
    comments = relationship("Comment", backref="user")


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)  # foreign key relates to user.id
    author = relationship("User", backref='comment')
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('blog_posts.id'),
        nullable=False)  # foreign key relates to blog_posts.id


db.create_all()
