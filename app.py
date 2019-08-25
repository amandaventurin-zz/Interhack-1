from flask import Flask, escape, request, redirect, render_template, g

app = Flask(__name__)

class Project:
  def __init__(self, title, image):
    self.title = title
    self.image = image

projects = [
  Project('Grace', '/static/img/grace.svg'),
  Project('Flower', '/static/img/card-top.jpg')
]

@app.route('/')
def hello():
  name = request.args.get('name', 'null')
  cool = name == 'Billy'
  return render_template('index.html', name=name, cool=cool)

@app.route('/feed/')
def feed():
  return render_template('feed.html', projects=projects)

@app.route('/<name>')
def foo(name):
  return render_template(name)


