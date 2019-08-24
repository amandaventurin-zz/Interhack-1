import os
import psycopg2
from flask import Flask, escape, request, redirect, render_template, g

app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL')

def get_db():
  if 'db' not in g:
    g.db = psycopg2.connect(database_url)
  
  return g.db

@app.teardown_appcontext
def teardown_db():
  db = g.pop('db', None)

  if db is not None:
    db.close()

@app.route('/')
def hello():
  name = request.args.get('name', 'null')
  cool = name == 'Billy'
  return render_template('index.html', name=name, cool=cool)
