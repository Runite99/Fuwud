from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from datetime import datetime
#from pyramid.response import FileResponse

import json
import requests
import mysql.connector as mysql
import os

# Email Imports
import smtplib, ssl
import codecs
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

REST_SERVER = os.environ['REST_SERVER']

db_host = "mysql-db"
db_name = 'fuwud'
db_user = 'admin'
db_pass = 'adminator'

def main_page(req):
  return render_to_response('home.html', {}, request=req)

# --- Navbar Routes
def get_compliments(req):
    return render_to_response('compliments.html',{}, request=req)

def get_terminal(req):
    return render_to_response('terminal.html',{}, request=req)

def get_hosting(req):
    return render_to_response('hosting.html',{}, request=req)

def get_status(req):
    return render_to_response('status.html',{}, request=req)

def get_questions(req):
    return render_to_response('questions.html',{}, request=req)

# --- Internal Routes
def get_directory(req):
    return render_to_response('directory.html', {}, request=req)

# --- Compliments Page Send to Backend + sends email with message
def send_compliment(receiver_email, name):
    password = FILLIN
    smtp_server = "smtp.gmail.com"
    sender_email = 'cibo.user@gmail.com'

    message = MIMEMultipart("alternative")
    message['Subject'] = 'You received a compliment!'
    message['From'] = sender_email
    message['To'] = receiver_email

    port = 587

    # part1 = MIMEText(text, 'plain')
    f = codecs.open('send_email.html', 'r', 'utf-8')
    f_string = f.read()
    html_string = f_string.replace('{NAME}', name)
    part2 = MIMEText(html_string, 'html')

    # message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def post_compliments(req):
    compliments = {
        'Name': req.params['Name'],
        'City': req.params['City'],
        'Email': req.params['Email']
    }
    print(compliments)
    print("Testing out dictionary access: Compliments\n")
    compliments_data = list(compliments.values())
    comp_name = compliments_data[0]
    comp_city = compliments_data[1]
    comp_email = compliments_data[2]
    now = datetime.now()
    comp_time = now.strftime('%Y-%m-%d %H:%M:%S')

    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()

    check_sql = f"SELECT * from Compliments where email = '{comp_time}'"
    
    sql = f"INSERT INTO Compliments (name, city, email, created_at, sent) VALUES ('{comp_name}', '{comp_city}', '{comp_email}', '{comp_time}', 0)"
    print(sql)
    cursor.execute(sql)
    db.commit()
    print(cursor.rowcount, "record inserted.")
    
    db.close()

    send_compliment(comp_email, comp_name)
    return render_to_response('compliments.html',{}, request=req)

if __name__ == '__main__':
#  config = Configurator()
    with Configurator() as config:

        config.include('pyramid_jinja2')
        config.add_jinja2_renderer('.html')

        config.add_route('main', '/')
        config.add_view(main_page, route_name='main')

        # --- Navbar Routes
        config.add_route('compliments', '/compliments')
        config.add_view(get_compliments, route_name='compliments', request_method='GET')
        config.add_view(post_compliments, route_name='compliments', request_method='POST')
        
        config.add_route('terminal', '/terminal')
        config.add_view(get_terminal, route_name='terminal')
        
        config.add_route('hosting', '/hosting')
        config.add_view(get_hosting, route_name='hosting')

        config.add_route('status', '/status')
        config.add_view(get_status, route_name='status')

        config.add_route('questions', '/questions')
        config.add_view(get_questions, route_name='questions')

        # --- Internal Routses
        config.add_route('directory', '/directory')
        config.add_view(get_directory, route_name='directory')


        config.add_static_view(name='/', path='./public', cache_max_age=3600)
        app = config.make_wsgi_app()
    
server = make_server('0.0.0.0', 5000, app)
server.serve_forever()
