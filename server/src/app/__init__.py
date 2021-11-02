# app/__init__.py
from flask import Flask

# initialize the app
app = Flask(__name__, instance_relative_config=True)

# load the views
from . import views

# load the configs -- this is already done in main based upon command line parameters and configs

