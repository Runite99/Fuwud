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
    message['Subject'] = 'multipart test'
    message['From'] = sender_email
    message['To'] = receiver_email

    port = 587

    text = f"""\
Subject: You've Been Complimented!


Howdy there {name}, my name is Doug Dimmadome owner of the Dimmsdale Dimmadome. 
Thank you for locating my long lost son Dale Dimmadome, heir to the Dimmsdale Dimmadome fortune. 
If there's anything I can do to repay you for your kindness, all you need to do is ask!"""

    html = """\
    <html>
    <body>
        <p>Hi,<br>
        How are you?<br>
        <a href="http://www.realpython.com">Real Python</a> 
        has many great tutorials.
        </p>
    </body>
    </html>
    """

    part1 = MIMEText(text, 'plain')
    f = codecs.open('send_email.html', 'r', 'utf-8')
    part2 = MIMEText(f.read(), 'html')

    message.attach(part1)
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

# #--- this is called to compare credentials to the value
# def is_valid_user(req):
#   username = req.params['email']
#   password = req.params['password']

#   print(username)
#   print(password)
#   Books = requests.get(REST_SERVER + "/books").json()
#   for x in Books:
#       user_db = x.get("username")
#       psswd_db = x.get("password")
#       if username == user_db and password == psswd_db:
#           return True

# #--- this route will validate login credentials...
# def post_login(req):
#   if is_valid_user(req) == True:
#     return render_to_response('did_login.html', {'error':'logged in.'}, request=req)
#   else:
#     return render_to_response('home.html', {'error':'Invalid Credentials'}, request=req)

# #--- this route will show a login form
# def get_login(req):
#     return render_to_response('home.html', {}, request=req)

# def get_signup_customer(req):
#     return render_to_response('signup.html',{}, request=req)

# def post_signup_customer(req):
#     user_data = {
#     'First Name': req.params['cust_f_name'],
#     'Last Name': req.params['cust_l_name'],
#     'Email': req.params['cust_email']
#     }
#     print(user_data)
#     print("Testing out dictionary access: Customer\n")
#     customer_data = list(user_data.values())
#     # customer_data[0] = '"'+ customer_data[0]+'"'
#     # customer_data[1] = '"'+ customer_data[1]+'"'
#     # customer_data[2] = '"'+ customer_data[2]+'"'

#     db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
#     print('Testing out DB')
#     cursor = db.cursor()
#     sql = "INSERT INTO Customers (first_name, last_name, email) VALUES (%s,%s,%s)"
#     val = ('"{0}","{1}","{2}"').format(customer_data[0], customer_data[1], customer_data[2])
#     print(val)
#     cursor.execute(sql, customer_data)
#     db.commit()
#     print(cursor.rowcount, "record inserted.")
#     db.close()
#     #requests.get()
#     #requests.post(REST_SERVER + "/books", json=user_data)
#     return render_to_response('did_login.html',{'error':'signed up.'}, request=req)
# def get_signup(req):
#     return render_to_response('signup.html',{}, request=req)

# def get_signup_printer(req):
#     return render_to_response('signup.html',{}, request=req)

# def post_signup_printer(req):
#     user_data = {
#     'First Name': req.params['print_f_name'],
#     'Last Name': req.params['print_l_name'],
#     'Email': req.params['print_email']
#     }
#     print(user_data)
#     print("Testing out dictionary access: Printer\n")
#     printer_data = list(user_data.values())
#     print(printer_data)

#     db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
#     print('Testing out DB')
#     cursor = db.cursor()
#     sql = "INSERT INTO Printers (first_name, last_name, email) VALUES (%s,%s,%s)"
#     val = ('"{0}","{1}","{2}"').format(printer_data[0], printer_data[1], printer_data[2])
#     print(val)
#     cursor.execute(sql, printer_data)
#     db.commit()
#     print(cursor.rowcount, "record inserted.")
#     db.close()
#     #requests.get()
#     #requests.post(REST_SERVER + "/books", json=user_data)
#     return render_to_response('did_login.html',{'error':'signed up.'}, request=req)

# def get_about(req):
#     return render_to_response('about.html',{}, request=req)

# def get_features(req):
#     return render_to_response('features.html',{}, request=req)

# def get_pricing(req):
#     return render_to_response('pricing.html',{}, request=req)

# def post_admin(req):
#     Books = requests.get(REST_SERVER + "/books").json()
#     print(req.params['confirm'])
#     string = req.params['confirm']
#     chooser = string.split('**')
#     chooser_data = {
#     'username': chooser[0],
#     'choose': chooser[1]
#     }

#     requests.post(REST_SERVER + "/button", json=chooser)
#     return render_to_response('show_admin.html',{'books': Books}, request=req)

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

        # config.add_route('login', '/login')
        # config.add_view(get_login, route_name='login', request_method='GET')
        # #config.add_view(post_login, route_name='login', request_method='POST')

        # config.add_route('signup','/signup')
        # config.add_view(get_signup, route_name='signup', request_method='GET')

        # config.add_route('signup_customer','/signup_customer')
        # config.add_view(get_signup_printer, route_name='signup_customer', request_method='GET')
        # config.add_view(post_signup_customer, route_name='signup_customer', request_method='POST')

        # config.add_route('signup_printer','/signup_printer')
        # config.add_view(get_signup, route_name='signup_printer', request_method='GET')
        # config.add_view(post_signup_printer, route_name='signup_printer', request_method='POST')

        # config.add_route('about','/about')
        # config.add_view(get_about, route_name='about', request_method='GET')

        # config.add_route('features','/features')
        # config.add_view(get_features, route_name='features', request_method='GET')

        # config.add_route('pricing','/pricing')
        # config.add_view(get_pricing, route_name='pricing', request_method='GET')
        #config.add_view(post_admin, route_name='admin', request_method='POST')

  #config.add_route("email", "/signup")
  #config.add_view(onSignUp, route_name1="email")
  #config.add_view(onSignup, route_name2="password")

        config.add_static_view(name='/', path='./public', cache_max_age=3600)
        app = config.make_wsgi_app()
server = make_server('0.0.0.0', 5000, app)
server.serve_forever()
