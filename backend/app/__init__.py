from flask import Flask

from .config import Config
from .extensions import bcrypt, db, migrate


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from . import models
    from .auth.routes import auth

    app.register_blueprint(auth, url_prefix="/api/auth")

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app
