from flask import Flask, escape, request, redirect, render_template, g

app = Flask(__name__)

@app.route('/')
def hello():
  name = request.args.get('name', 'null')
  cool = name == 'Billy'
  return render_template('index.html', name=name, cool=cool)

@app.route('/<name>')
def foo(name):
  return render_template(name)

