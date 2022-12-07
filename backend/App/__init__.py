from flask import Flask
from . import views

def app_init():
  app = Flask(__name__)
  app.config["SECRET_KEY"] = "F22_SLFL"
  app.register_blueprint(views.main_bp)
  return app