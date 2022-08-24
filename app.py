#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'komorebi'
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.orm import relationship
from flask_gravatar import Gravatar
import os
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

Bootstrap(app)

# flask_ckeditor
ckeditor = CKEditor(app)
# CONNECT TO DB
uri = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
if uri and uri.startswith("postgres://"):
    uri.replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# flask_login
login_manager = LoginManager()
login_manager.init_app(app)

# flask_gravatar
gravatar = Gravatar(app)
