from flask import Flask, escape, request, redirect, render_template, g
import re

app = Flask(__name__)

new_pid = 0

class Project:
  
  def __init__(
    self,
    title,
    image,
    plogo,
    tags,
    desc,
    processo_seletivo,
    contato,
    universidade,
    campus,
    instituto,
    curso,
    periodo,
    bolsa):
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
    self.bolsa = bolsa
    self.plogo = plogo

projects = [
  Project(
    title='Grace',
    image='/static/img/GRACE_logo.svg',
    plogo='/static/img/grace.svg',
    tags={'Mulheres', 'Computação', 'Empreendedorismo'},
    desc='Garotas na computação e Empreendedorismo',
    universidade='USP',
    campus='USP Leste',
    instituto='EACH',
    curso='SI',
    periodo='Flexível',
    processo_seletivo='',
    contato='190',
    bolsa=True),
  Project(
    title='PET SI',
    image='/static/img/pet-si.jpg',
    plogo='/static/img/pet-logo.jpg',
    tags={'SI', 'Educação', 'Bolsas'},
    desc='Programa de Educação Tutorial',
    universidade='USP',
    campus='USP Leste',
    instituto='EACH',
    curso='SI',
    periodo='Flexível',
    processo_seletivo='',
    contato='190',
    bolsa=False),
  Project(
    title='USPCodeLab',
    image='/static/img/ucl-header.svg',
    plogo='/static/img/ucl-logo.svg',
    tags={'SI', 'BCC', 'Hackathon'},
    desc='Grupo de extensão que visa estimular a inovação tecnológica na USP',
    universidade='USP',
    campus='',
    instituto='Todos',
    curso='SI',
    periodo='Flexível',
    processo_seletivo='',
    contato='190',
    bolsa=False)
]

def search(
  projects,
  tags=set(),
  universidade='',
  campus='',
  instituto='',
  curso='',
  titulo='',
  periodo='',
  bolsa=False):
  ret = []

  if periodo == 'Flexível':
    periodo = ''

  for p in projects:
    uni = re.compile(universidade)
    cam = re.compile(campus)
    ins = re.compile(instituto)
    cur = re.compile(curso)
    per = re.compile(periodo)
    tit = re.compile(titulo)

    if not p.tags.issuperset(tags): continue
    if uni.search(p.universidade) is None: continue
    if cam.search(p.campus) is None: continue
    if ins.search(p.instituto) is None: continue
    if cur.search(p.curso) is None: continue
    if per.search(p.periodo) is None: continue
    if tit.search(p.title) is None: continue
    if bolsa and not p.bolsa: continue

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
  uni = form.get('pesquisar-universidade')
  cam = form.get('pesquisar-campus')
  ins = form.get('pesquisar-instituto')
  cur = form.get('pesquisar-curso')
  tit = form.get('pesquisar-pesquisar')
  per = form.get('pesquisar-periodo')
  bol = form.get('pesquisar-bolsa') == 'ok'

  p = search(
    projects=projects,
    tags=set(),
    universidade=uni,
    campus=cam,
    instituto=ins,
    curso=cur,
    titulo=tit,
    periodo=per,
    bolsa=bol)
  return render_template('feed.html', projects=p)

@app.route('/form-add/', methods=['POST'])
def form_add():
  form = request.form
  uni = form.get('novop-universidade')
  cam = form.get('novop-campus')
  ins = form.get('novop-instituto')
  cur = form.get('novop-curso')
  per = form.get('novop-periodo')
  des = form.get('novop-descricao')
  pro = form.get('novop-processo')
  con = form.get('novop-contato')
  tit = form.get('novop-titulo')

  projects.append(Project(
    title=tit,
    image='/static/img/add_img.png',
    plogo='/static/img/add_img.png',
    tags={'TAG'},
    desc=des,
    universidade=uni,
    campus=cam,
    instituto=ins,
    curso=cur,
    periodo=per,
    processo_seletivo=pro,
    contato=con,
    bolsa=True))
  return redirect('/feed/')