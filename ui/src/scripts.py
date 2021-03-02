import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv('credentials.env')

import mysql.connector as mysql
# Email Imports
import smtplib, ssl
import codecs
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

db_host = "mysql-db"
db_name = os.environ['MYSQL_DATABASE']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']

def send_compliment(receiver_email, name):
    print("This ran")
    smtp_server = "smtp.gmail.com"
    password = os.environ['EMAIL_PASSWORD']
    sender_email = os.environ['EMAIL']

    message = MIMEMultipart("alternative")
    message['Subject'] = 'You received a compliment!'
    message['From'] = sender_email
    message['To'] = receiver_email

    port = 587

    # part1 = MIMEText(text, 'plain')
    f = codecs.open('html_files/send_email.html', 'r', 'utf-8')
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

def compliments_to_db(compliments_data):
    comp_name = compliments_data[0]
    comp_city = compliments_data[1]
    comp_email = compliments_data[2]
    now = datetime.now()
    comp_time = now.strftime('%Y-%m-%d %H:%M:%S')

    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()

    check_sql = f"SELECT * from Compliments where email = '{comp_time}'"
    
    sql = f"INSERT INTO Compliments (name, city, email, created_at) VALUES ('{comp_name}', '{comp_city}', '{comp_email}', '{comp_time}')"
    print(sql)
    cursor.execute(sql)
    db.commit()
    print(cursor.rowcount, "record inserted.")
    
    db.close()