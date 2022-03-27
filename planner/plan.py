from . import db
import datetime
from flask import Flask, g, flash, Blueprint, render_template, request, redirect, url_for, session
from flask_session import Session

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
    session["username"] = username
    cursor.execute("""select password from users where username = %s;""", (username,))
    pw = cursor.fetchone()
    if pw[0] != password:
      status = 'Incorrect password, please try again'
    else:
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




@bp.route('/today', methods=['POST', 'GET'])
def today():





@bp.route('/addtask', methods=['POST', 'GET'])
def add_task():





def delete_task():





@bp.route('/shopping', methods=['POST', 'GET'])
def shopping():



