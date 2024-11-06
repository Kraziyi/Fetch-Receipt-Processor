from flask import Flask
from app.controllers import receipts_blueprint
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(receipts_blueprint, url_prefix='/receipts')
    return app
