import os
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from pkg.config import DevelopmentConfig

load_dotenv()

def create_app():
    from pkg.models import db

    app = Flask(__name__, static_folder= 'static')

    app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    migrate = Migrate(app, db)

    return app

app = create_app()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

from pkg import routes