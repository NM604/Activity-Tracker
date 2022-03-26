import os
from flask import Flask, render_template, flash
import psycopg2

from . import db

def createapp(test_config=None):

  app = Flask("planner")
  app.secretkey = "super_secret"
  app.config.from_mapping(DATABASE = "plannerdata")
  
  if (test_config is not None):
    app.config.update(test_config)
  
  os.makedirs(app.instance_path)
  
  except OSError:
    pass
    
  from . import plan
  app.register_blueprint(plan.bp)
  
  from . import db
  db.init_app(app)
  
  return app
