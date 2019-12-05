from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
from flask.cli import with_appcontext
import click

__version__ = (0, 0, 1, "dev")

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    """DEV SIZE"""
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['TMP_STORAGE'] = os.path.join(app.instance_path, 'tmp')

    db_url = os.environ.get('DATABASE_URL')

    """check if not set `db_url` environment"""
    if db_url is None:
        db_url = "sqlite:///{}".format(
            os.path.join(app.instance_path, "db.sqlite"))
        os.makedirs(app.instance_path, exist_ok=True)

    """create tmp dir for uploads"""
    os.makedirs(app.config['TMP_STORAGE'], exist_ok=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("secret", "dev"),  # change this in prod
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        # load prod config
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load dev config
        app.config.update(test_config)

    db.init_app(app)
    app.cli.add_command(init_db_command)
    
    with app.app_context():
        from dmcode_server import files, frontend

        app.register_blueprint(files.bp)
        app.register_blueprint(frontend.bp)

        app.add_url_rule('/', endpoint='index')

    return app


def init_db():
    db.drop_all()
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """delete all data and create new tables"""
    init_db()
    click.echo("init db")

