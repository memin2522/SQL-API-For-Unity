from flask import Flask 
from ip_whitelist import grant_access
from . import db
from .routes import main

def create_app():
    app = Flask(__name__)

    app.config.from_prefixed_env()
    grant_access.fill_whitelist_dict()
    
    db.init_app(app)
    app.register_blueprint(main)

    return app