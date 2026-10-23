from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import bcrypt, db, migrate

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from . import models
    from .auth.routes import auth
    from .notes.routes import notes

    app.register_blueprint(auth, url_prefix="/api/auth")
    app.register_blueprint(notes, url_prefix="/api/notes")

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app
