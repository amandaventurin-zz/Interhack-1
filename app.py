from flask import Flask, escape, request, redirect, render_template, g
import re

app = Flask(__name__)

class Project:
  
  def __init__(
    self,
    title,
    image,
    tags,
    desc,
    universidade,
    campus,
    instituto,
    curso):
    self.title = title
    self.image = image
    self.tags  = tags
    self.desc  = desc
    self.universidade = universidade
    self.campus = campus
    self.instituto = instituto
    self.curso = curso

projects = [
  Project(
    title='Grace',
    image='/static/img/grace.svg',
    tags=set(),
    desc='aaaaaa',
    universidade='USP',
    campus='USP Leste',
    instituto='EACH',
    curso='SI'),
  Project(
    title='Flower',
    image='/static/img/card-top.jpg',
    tags={'SAUDE'},
    desc='',
    universidade='USP',
    campus='USP Leste',
    instituto='EACH',
    curso='TM')
]

def search(
  projects,
  tags,
  universidade,
  campus,
  instituto,
  curso):
  ret = []
  for p in projects:
    uni = re.compile(universidade)
    cam = re.compile(campus)
    ins = re.compile(instituto)
    cur = re.compile(curso)

    if not p.tags.issuperset(tags): continue
    if uni.search(p.universidade) is None: continue
    if cam.search(p.campus) is None: continue
    if ins.search(p.instituto) is None: continue
    if cur.search(p.curso) is None: continue

    ret.append(p)
  return ret

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

@app.route('/form-test/', methods=['POST'])
def form_test():
  form = request.form
  #return f'{form}'
  tags = set()
  if form.get('tag-saude')   == 'on': tags.add('SAUDE') 
  if form.get('tag-lgbt')    == 'on': tags.add('LGBT') 
  if form.get('tag-esporte') == 'on': tags.add('ESPORTE') 
  uni = form.get('universidade')
  cam = form.get('campus')
  ins = form.get('instituto')
  cur = form.get('curso')

  p = search(
    projects=projects,
    tags=tags,
    universidade=uni,
    campus=cam,
    instituto=ins,
    curso=cur)
  return render_template('feed.html', projects=p)
