# import sqlalchemy
# from   sqlalchemy.ext.automap import automap_base
# from   sqlalchemy.orm         import Session
# from   sqlalchemy             import create_engine, func

import numpy as np
from flask import render_template, flash, redirect, url_for, request, Flask, jsonify
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.auth.forms import LoginForm
from app.models import User, ProjectSummary, ProjectPerformanceRatings
from flask_login import current_user, login_user, logout_user, login_required
import sys

#/******************************************************************************/
@bp.route('/login', methods=['GET', 'POST'])
def login():
    sys.stdout.write("In /login view method")
    sys.stdout.flush()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

#/******************************************************************************/
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

#/******************************************************************************/