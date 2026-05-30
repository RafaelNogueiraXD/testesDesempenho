from flask import Flask
from flask_cors import CORS
from .database import engine, Base
from .routes import bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    Base.metadata.create_all(bind=engine)

    app.register_blueprint(bp)

    return app
