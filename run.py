from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)

    from logistica.routes import main
    app.register_blueprint(main)

    return app

from logistica import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)