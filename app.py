from flask import Flask, escape, request, redirect, render_template, g
import re

app = Flask(__name__)

new_pid = 0

class Project:
  
  def __init__(
    self,
    title,
    image,
    tags,
    desc,
    processo_seletivo,
    contato,
    universidade,
    campus,
    instituto,
    curso,
    periodo):
    global new_pid
    self.pid = new_pid
    new_pid += 1
    self.title = title
    self.image = image
    self.tags  = tags
    self.desc  = desc
    self.universidade = universidade
    self.campus = campus
    self.instituto = instituto
    self.curso = curso
    self.processo_seletivo = processo_seletivo
    self.periodo = periodo
    self.contato = contato

projects = [
  Project(
    title='Grace',
    image='/static/img/grace.svg',
    tags=set(),
    desc='aaaaaa',
    universidade='USP',
    campus='USP Leste',
    instituto='EACH',
    curso='SI',
    periodo='Flexivel',
    processo_seletivo='dsds',
    contato='190'),
  Project(
    title='Flower',
    image='/static/img/card-top.jpg',
    tags={'SAUDE'},
    desc='uuuuuu',
    universidade='USP',
    campus='USP Leste',
    instituto='EACH',
    curso='TM',
    periodo='Flexivel',
    processo_seletivo='dsds',
    contato='190')
]

def search(
  projects,
  tags=set(),
  universidade='',
  campus='',
  instituto='',
  curso=''):
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

def search_pid(projects, pid):
  for p in projects:
    if p.pid == pid: return p 

@app.route('/')
def hello():
  return render_template('index.html')

@app.route('/feed/')
def feed():
  return render_template('feed.html', projects=projects)

@app.route('/projeto/')
def projeto():
  pid = int(request.args.get("pid", None))
  p = search_pid(projects, pid)
  return render_template('projeto.html', project = p)

@app.route('/pesquisar/')
def pesquisa():
  return render_template('pesquisar.html')

@app.route('/login/')
def login():
  return render_template('login.html')

@app.route('/novo_projeto/')
def novo_projeto():
  return render_template('novo_projeto.html', project=search_pid(projects, 0))

@app.route('/<name>')
def foo(name):
  return render_template(name)


@app.route('/form-search/', methods=['POST'])
def form_search():
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

@app.route('/form-add/', methods=['POST'])
def form_add():
  form = request.form
  uni = form.get('novop-universidade')
  cam = form.get('novop-campus')
  ins = form.get('novop-instituicao')
  cur = form.get('novop-curso')
  per = form.get('novop-periodo')
  des = form.get('novop-descricao')
  pro = form.get('novop-processo')
  con = form.get('novop-contato')
  tit = form.get('novop-titulo')

  projects.append(Project(
    title=tit,
    image='/static/img/add_img.png',
    tags={'SAUDE'},
    desc=des,
    universidade=uni,
    campus=cam,
    instituto=ins,
    curso=cur,
    periodo=per,
    processo_seletivo=pro,
    contato=con))
  return f'{form}'