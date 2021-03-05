from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.view import view_config
from scripts import send_compliment, compliments_to_db, newsletter_to_db

import json
import requests
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
    print(req.params)
    compliments = {
        'first_name': req.params['first_name'],
        'last_name': req.params['last_name'],
        'chef_first_name': req.params['chef_first_name'],
        'chef_last_name': req.params['chef_last_name'],
        'city': req.params['city'],
        'email': req.params['email'],
        'anon': req.params['anon'],
        'news': req.params['news'],
    }
    print(compliments)
    compliments_to_db(compliments)
    send_compliment(compliments['email'], compliments['chef_first_name'])
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


# --- Newsletter Page
@view_config(route_name='newsletter_signup', request_method='GET')
def get_newsletter_signup(req):
    return render_to_response('html_files/newsletter_signup.html', {}, request=req)

@view_config(route_name='newsletter_signup', request_method='POST')
def post_newsletter_signup(req):
    print(req.params)
    newsletter_signup = {
        'first_name': req.params['first_name'],
        'last_name': req.params['last_name'],
        'mobile': req.params['mobile'],
        'email': req.params['mail'],
    }
    for key in newsletter_signup:
        if newsletter_signup[key] == '':
            newsletter_signup[key] = None
    valid = newsletter_to_db(newsletter_signup)
    # send_compliment(compliments['email'], compliments['chef_first_name'])
    if valid is True:
        return render_to_response('html_files/newsletter_signup.html',{}, request=req)
    else:
        return render_to_response('html_files/newsletter_signup_duplicate.html',{}, request=req)