from . import db
import datetime
from flask import Flask, g, flash, Blueprint, render_template, request, redirect, url_for

bp = Blueprint('plan', 'plan', url_prefix = '')

@bp.route('/')
def dashboard():
  return render_template("login.html", url_prefix="")
  

