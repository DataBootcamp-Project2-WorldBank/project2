import sqlalchemy
from   sqlalchemy.ext.automap import automap_base
from   sqlalchemy.orm         import Session
from   sqlalchemy             import create_engine, func

import numpy as np

from flask import render_template, flash, redirect, url_for, request, Flask, jsonify
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm
from app.models import User, ProjectSummary, ProjectPerformanceRatings
from flask_login import current_user, login_user, logout_user, login_required
import sys

#/******************************************************************************/
@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

#/******************************************************************************/
@app.route('/login', methods=['GET', 'POST'])
def login():
    sys.stdout.write("In /login view method")
    sys.stdout.flush()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

#/******************************************************************************/
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/iegdataview')
@login_required
def iegdataview():
    return render_template('iegDataView.html', title='Data')

@app.route('/iegdata')
@login_required
def iegdata():
    return render_template('iegData.html', title='table')

@app.route('/gdpdataview')
@login_required
def gdpdataview():
    return render_template('gdpDataView.html', title='Data')

@app.route('/gdpdata')
@login_required
def gdpdata():
    return render_template('gdpData.html', title='table')

@app.route('/popdataview')
@login_required
def popdataview():
    return render_template('popDataView.html', title='Data')

@app.route('/populationdata')
@login_required
def populationdata():
    return render_template('populationData.html', title='table')

@app.route('/cpidataview')
@login_required
def cpidataview():
    return render_template('cpiDataView.html', title='Data')

@app.route('/cpidata')
@login_required
def cpidata():
    return render_template('cpiData.html', title='table')

@app.route('/gdpanalysis')
@login_required
def gdpanalysis():
    return render_template('gdp_analysis.html', title='GDP Analysis')

@app.route('/poplevel')
@login_required
def poplevel():
    return render_template('population_level.html', title='Population Level Analysis')


#/******************************************************************************/

@app.route("/api/v1.0/summary")
def summary():
    results = ProjectSummary.query.all()
    response = []
        
    for rec in results:
        record_dict                 = {}
        record_dict["region"]         = rec.region
        record_dict["country_code_a2"]   = rec.country_code_a2
        record_dict["country_code_a3"]   = rec.country_code_a3
        record_dict["country_name"]   = rec.country_name
        record_dict["total"]          = rec.total
        record_dict["satisfactory"]   = rec.satisfactory
        record_dict["unsatisfactory"] = rec.unsatisfactory
        record_dict["unavailable"]    = rec.unavailable
        response.append(record_dict)

    return jsonify(response)

#******************************************************************************/
@app.route("/api/v1.0/project/<country_code>")
def getProjects(country_code):
    response = []
    #Find the 2 letter country code that matches the passed country_code (3-letter).
    project_summary_record = ProjectSummary.query.filter_by(country_code_a3=country_code).first()
    if (project_summary_record):
        country_code_a2 = project_summary_record.country_code_a2
        canonalized = country_code_a2.upper()   
        if(canonalized):
            results =  ProjectPerformanceRatings.query.filter_by(country_code=canonalized).all()
            response = [] 
            for rec in results:
                record_dict                      = {}
                record_dict["project_id"]        = rec.project_id
                record_dict["project_name"]      = rec.project_name
                record_dict["region"]            = rec.region
                record_dict["country_code"]      = rec.country_code
                record_dict["country_name"]      = rec.country_name
                record_dict["project_cost"]      = rec.project_cost
                record_dict["IEG_outcome"]       = rec.IEG_outcome
                response.append(record_dict)

    return jsonify(response)

