import sqlalchemy
from   sqlalchemy.ext.automap import automap_base
from   sqlalchemy.orm         import Session
from   sqlalchemy             import create_engine, func
import os

import numpy as np

from flask import render_template, flash, redirect, url_for, request, \
     Flask, jsonify, current_app
from flask_login import current_user, login_user, logout_user, \
     login_required
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.auth.forms import LoginForm
from app.main.forms import PostForm
from app.models import User, ProjectSummary, ProjectPerformanceRatings
from app.main import bp

import sys
import scrape_ieg


#/**************************************************************************
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Home')


#/**************************************************************************

@bp.route('/iegdataview')
@login_required
def iegdataview():
    heroku_deploy = os.environ.get('HEROKU_DEPLOY')
    if ( heroku_deploy == "N" or heroku_deploy == "n"):
        scrape_ieg.scrape_info()
        return render_template('iegDataView.html', title='Data')
    else:
        return render_template('iegData.html', title='table')


@bp.route('/iegdata')
@login_required
def iegdata():
    return render_template('iegData.html', title='table')

@bp.route('/gdpdataview')
@login_required
def gdpdataview():
    return render_template('gdpDataView.html', title='Data')

@bp.route('/gdpdata')
@login_required
def gdpdata():
    return render_template('gdpData.html', title='table')

@bp.route('/popdataview')
@login_required
def popdataview():
    return render_template('popDataView.html', title='Data')

@bp.route('/populationdata')
@login_required
def populationdata():
    return render_template('populationData.html', title='table')

@bp.route('/cpidataview')
@login_required
def cpidataview():
    return render_template('cpiDataView.html', title='Data')

@bp.route('/cpidata')
@login_required
def cpidata():
    return render_template('cpiData.html', title='table')

@bp.route('/gdpanalysis')
@login_required
def gdpanalysis():
    return render_template('gdp_analysis.html', title='GDP Analysis')

@bp.route('/poplevel')
@login_required
def poplevel():
    return render_template('population_level.html', title='Population Level Analysis')

@bp.route('/cpilevel')
@login_required
def cpilevel():
    return render_template('cpi_level.html', title='Corruption Index Level Analysis')

@bp.route('/gdplevel')
@login_required
def gdplevel():
    return render_template('gdp_level.html', title='GDP Level Analysis')

@bp.route('/aboutproject')
@login_required
def aboutproject():
    return render_template('aboutProject.html', title='About Project')
#/******************************************************************************/

@bp.route("/api/v1.0/summary")
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
        record_dict["avg_population"] = rec.avg_population
        record_dict["gdp"] = rec.gdp
        record_dict["cpi"] = rec.cpi
        response.append(record_dict)
    return jsonify(response)

#******************************************************************************/
@bp.route("/api/v1.0/project/<country_code>")
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