from . import db
import datetime
from flask import Flask, g, flash, Blueprint, render_template, request, redirect, url_for, session
from flask_session import Session

bp = Blueprint('plan', 'plan', url_prefix = '')



@bp.route('/')
def dashboard():
  if not session.get("username"):
    return redirect("/login")
  return render_template("dashboard.html", url_prefix="")
  
  

@bp.route('/login', methods=['POST', 'GET'])  
def login():
  conn = db.get_db()
  cursor = conn.cursor()
  status = None
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    session["username"] = username
    cursor.execute("""select pass from users where username = %s;""", (username,))
    pw = cursor.fetchone()
    if pw[0] != password:
      status = 'Incorrect password, please try again'
    else:
      return redirect('/', 302)
    return render_template('login.html', status = status)
    
    
    
    
@bp.route('/logout')
def logout():
  session["username"] = None
  return redirect("/", 302)   
  
  
   
    
@bp.route('/create')
def create():
  return render_template('create.html')
  
  
  
  
@bp.route('/createuser', methods=['POST', 'GET'])
def createuser():
  username = request.form['username']
  password = request.form['password']
  conn = db.get_db()
  cur = conn.cursor()
  cur.execute("""select username from users where username = %s;""", (username,))
  n = cur.fetchone()
  if n is not None:
    flash('Username already exists')
    return redirect('/create', 302)
  cursor.execute("""insert into users (username, password) values (%s, %s);""", (username, password))
  conn.commit()
  return redirect('/login', 302)
  
  
  
  

