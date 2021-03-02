from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

import json
import mysql.connector as mysql
import os

db_host = "mysql-db"
db_name = '140b_rest_db'
db_user = 'admin'
db_pass = 'adminator'

def get_students_method(req):
  # Connect to the database and retrieve the student
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  print('Test')
  cursor = db.cursor()
  cursor.execute("select id, firstname, lastname, email, pid from Users;")
  records = cursor.fetchall()
  return json.dumps(records)

def get_users(req):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT count(id) from Users;")
    records = cursor.fetchall()
    return json.dumps(records)

def get_users_age(req):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT AVG(age) from Users;")
    records = str(cursor.fetchall())
    return json.dumps(records)

def get_courses_users(req):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT course_id, COUNT(id) FROM Enrollments GROUP BY course_id;")
    records = cursor.fetchall()
    return json.dumps(records)

def get_course_students(req):
  the_id = req.matchdict['course']
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  if the_id == 'ECE140':
    cursor.execute("SELECT Enrollments.course_id, Enrollments.student_id, Users.firstname, Users.lastname FROM Enrollments INNER JOIN Users ON Enrollments.student_id=Users.id AND Enrollments.course_id=1;")
    record = cursor.fetchall()
    return json.dumps(record)

  if the_id == 'ECE141':
    cursor.execute("SELECT Enrollments.course_id, Enrollments.student_id, Users.firstname, Users.lastname FROM Enrollments INNER JOIN Users ON Enrollments.student_id=Users.id AND Enrollments.course_id=2;")
    record = cursor.fetchall()
    return json.dumps(record)

def get_students(req):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT count(student_id) AS students, Courses.coursename, Users.firstname, Users.lastname FROM Enrollments JOIN Courses ON Enrollments.course_id=Courses.id JOIN Users ON Courses.prof_id=Users.id GROUP BY course_id;")
    records = cursor.fetchall()
    return json.dumps(records)

def get_student_method(req):
  # Retrieve the route argument (this is not GET/POST data!)
  the_id = req.matchdict['student_id']

  # Connect to the database and retrieve the student
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select * from TUsers where id='%s';" % the_id)
  record = cursor.fetchone()
  db.close()

  if record is None:
    return ""

  # Format the result as key-value pairs
  response = {
    'id':         record[0],
    'first_name': record[1],
    'last_name':  record[2],
    'email':      record[3],
    'pid':        record[4],
    'datetime':   record[5].isoformat()
  }
  return json.dumps(response)


''' Route Configurations '''
if __name__ == '__main__':
  config = Configurator()

  config.add_route('users_count', '/users/count')
  config.add_view(get_users, route_name='users_count', renderer='json')

  config.add_route('users_age', '/users/age')
  config.add_view(get_users_age, route_name='users_age', renderer='json')

  config.add_route('courses_users', '/courses/users')
  config.add_view(get_courses_users, route_name='courses_users', renderer='json')

  config.add_route('student_course', '/students/{course}')
  config.add_view(get_course_students, route_name='student_course', renderer='json')

  config.add_route('get_student', '/student/{student_id}')
  config.add_view(get_student_method, route_name='get_student', renderer='json')

  config.add_route('get_students', '/students')
  config.add_view(get_students, route_name='get_students', renderer='json')

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()