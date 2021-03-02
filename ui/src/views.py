from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.view import view_config
from scripts import send_compliment, compliments_to_db

import json
import requests
import mysql.connector as mysql
import os

@view_config(route_name='main')
def main_page(req):
    return render_to_response('html_files/home.html', {}, request=req)

# --- Navbar Routes
@view_config(route_name='compliments', request_method='GET')
def get_compliments(req):
    return render_to_response('html_files/compliments.html',{}, request=req)

@view_config(route_name='compliments', request_method='POST')
def post_compliments(req):
    compliments = {
        'Name': req.params['Name'],
        'City': req.params['City'],
        'Email': req.params['Email']
    }
    compliments_data = list(compliments.values())
    compliments_to_db(compliments_data)
    send_compliment(req.params['Email'], req.params['Name'])
    return render_to_response('html_files/compliments.html',{}, request=req)

@view_config(route_name='terminal')
def get_terminal(req):
    return render_to_response('html_files/terminal.html',{}, request=req)

@view_config(route_name='hosting')
def get_hosting(req):
    return render_to_response('html_files/hosting.html',{}, request=req)

@view_config(route_name='status')
def get_status(req):
    return render_to_response('html_files/status.html',{}, request=req)

@view_config(route_name='questions')
def get_questions(req):
    return render_to_response('html_files/questions.html',{}, request=req)

# --- Internal Routes
@view_config(route_name='directory')
def get_directory(req):
    return render_to_response('html_files/directory.html', {}, request=req)