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
      status = 'Incorrect password, please try again'
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
  fmonth = request.args.get("m",1)
  if int(fmonth)<10:
    x = str(fmonth)
    fmonth = '0'+x
  fyear = request.args.get("y",1)
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
  
  


