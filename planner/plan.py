from . import db
import datetime
from flask import Flask, g, flash, Blueprint, render_template, request, redirect, url_for, session
from flask_session import Session
from datetime import date

bp = Blueprint('plan', 'plan', url_prefix = '')



@bp.route('/')
def dashboard():
  if not session.get("username"):
    return redirect(url_for("plan.login"))
  return render_template("dashboard.html")
  
  

@bp.route('/login', methods=['POST', 'GET'])  
def login():
  conn = db.get_db()
  cursor = conn.cursor()
  status = None
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    cursor.execute("""select password from users where username = %s;""", (username,))
    pw = cursor.fetchone()
    if pw[0] != password:
      status = 'Incorrect password'
    else:
      cursor.execute("""select id from users where username = %s;""", (username,))
      user = cursor.fetchone()
      userid = user[0]
      session["username"] = username
      session["id"] = userid
      return redirect('/', 302)
  if status is not None:
    return render_template('login.html', status = status)
  else:
    return render_template('login.html')
    
    
    
    
@bp.route('/logout')
def logout():
  session["username"] = None
  session["id"] = None
  return redirect("/", 302)   
  
  
   
    
@bp.route('/create')
def create():
  return render_template('create.html')
  
  
  
  
@bp.route('/createuser', methods=['POST'])
def createuser():
  status = None
  username = request.form['username']
  password = request.form['password']
  conn = db.get_db()
  cur = conn.cursor()
  cur.execute("""select username from users where username = %s;""", (username,))
  n = cur.fetchone()
  if n is not None:
    flash('Username already exists')
    return redirect(url_for("plan.create"), 302)
  cur.execute("""insert into users (username, password) values (%s, %s);""", (username, password))
  conn.commit()
  return redirect('/', 302)





@bp.route('/calender')
def calender():
  
  listtasks = None
  conn = db.get_db()
  cursor = conn.cursor()
  user_id = session.get("userid")
  fday = request.args.get("d",1)
  if int(fday)<10:
    r = str(fday)
    fday = '0'+r
  fmonth = request.args.get("d",1)
  if int(fmonth)<10:
    x = str(fmonth)
    fmonth = '0'+x
  fyear = request.args.get("d",1)
  ffdate = str(fyear)+'-'+fmonth+'-'+fday
  
  current_time = datetime.datetime.now() 
  year = current_time.year
  month = current_time.month
  day = current_time.day
  current = date.today()
  today = current.strftime("%A")
  fdate = current.strftime("%B %d")
  m = current.strftime("%m")
  
  for i in range(0,31):
    if i == request.args.get("d"):
      cursor.execute("""select name from tasks where oid = %s and deadline = %s;""", (user_id, ffdate))
  
  return render_template('calender.html', year=year,month=month,day=day,today=today,fdate=fdate, m=m, listtasks=listtasks, fday=fday, fmonth=fmonth, fyear=fyear)
  
  


@bp.route('/thisday')
def thisday():
  conn = db.get_db()
  cursor = conn.cursor()
  this_day = request.args.get("d",1)
  this_month = request.args.get("d",1)
  this_year = request.args.get("d",1)
  
  if int(this_day)<10:
    r = str(this_day)
    this_day = '0'+r
  
  if int(this_month)<10:
    x = str(this_month)
    this_month = '0'+x
    
  this_date = str(fyear)+'-'+fmonth+'-'+fday
  cursor.execute("""select name, description, deadline from tasks where oid = %s and deadline = %s;""", (user_id, this_date))
  info = cursor.fetchall()
  return render_template('thisday.html',info=info)
  
  
  
  
@bp.route('/addtask')
def add_task():
  return render_template('add_task.html')


 
@bp.route('/addtaskdetails', methods=['POST', 'GET'])
def add_taskdetails():
  if request.method == 'POST':
    name = request.form['name']
    description = request.form['description']
    deadline = request.form['deadline']
    oid = session.get("userid")
    shopping_status = request.form['shopping_status']
    conn = db.get_db()
    cursor = conn.cursor()
    
    cursor.execute("""insert into tasks (name, description, deadline, oid, shopping) values (%s, %s, %s, %s);""", (name, description, deadline, oid, shopping_status))
    
    conn.commit()
    
    if shopping_status=='y' or shopping_status=='Y':
      cursor.execute("""select id from tasks where name = %s;""",(name,))
      taskid = cursor.fetchone()
      tid = taskid[0]
      session["tid"] = tid
      session["deadline"] = deadline
      conn.commit()
      redirect(url_for("plan.shopping"))
    conn.commit()
    return redirect(url_for("plan.calender"))
    
    
    
    
    
@bp.route('/shopping')
def shopping():
  return render_template('shopping.html')    
  
  
  
  
    
@bp.route('/additems', methods=['POST', 'GET'])
def add_taskdetails():  
  conn = db.get_db()
  cursor = conn.cursor()
  tid = session.get("tid")
  deadline = session.get("deadline")
  
  if request.method == 'POST':
  
    itemname = request.form['itemname']
    itemquant = request.form['itemquant']
    cursor.execute("""insert into shoppinglist (item, qty, tid, deadline) values (%s, %s, %s, %s);""", (itemname, itemquant, tid, deadline))
    conn.commit()
  
    status = request.form['status']
    
    if status == 'y' or status == 'Y':
      session["tid"] = None
      session["deadline"] = None
      conn.commit()
      return redirect(url_for("plan.calender")    
    conn.commit()
    return redirect(url_for("plan.additems"))
    
    
    
    
@bp.route('/deletetask', methods=['POST', 'GET'])
def deletetask():
  if request.method == 'POST':
    name = request.form['name']
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("""delete from tasks where name = %s;""",(name,))
    cursor.execute("""select shopping from tasks where name = %s;""",(name,))
    shoppingstatus = cursor.fetchone()
    shop_status = shoppingstatus[0]
    if shop_status == 'y':
      cursor.execute("""select id from tasks where name = %s;""",(name,))
      t = cursor.fetchone()
      tasksid = t[0]
      cursor.execute("""delete from shoppinglist where tid = %s;""",(tasksid,))
    conn.commit()
    return redirect(url_for("plan.calender"))
    
    
    
    
@bp.route('/update')
def update():
  conn = db.get_db()
  cursor = conn.cursor()
  dtime = datetime.datetime.now().strftime("%Y-%m-%d")
  cursor.execute("""delete from tasks where deadline = %s;""",(dtime,))
  cursor.execute("""select shopping from tasks where deadline = %s;""",(deadline,))
  conn.commit()
  return redirect(url_for("plan.calender"))

  
