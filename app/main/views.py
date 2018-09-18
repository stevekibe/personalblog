from flask import render_template, request, redirect, url_for, abort
from . import main
from .. import db
from ..models import User
from flask_login import login_required,current_user


@main.route('/')
def index():
    '''
    method to the root page
    ''' 
    

    title = 'Home- Welcome'
    return render_template('index.html', title = title,)

@main.route('')