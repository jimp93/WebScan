import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

# can't directly register with app as the app is not global. Don't want to do it directly in factory as will be stuck
db = SQLAlchemy()


# make a command line instruction for creating tables
def init_app_inst(app):
    app.cli.add_command(init_db_command)


# Commands added using the Flask app’s cli command() decorator will be executed with an application context pushed,
#  so your command and extensions have access to the app and its configuration. If you create a command using the
# Click command() decorator instead of the Flask decorator, you can use with_appcontext() to get the same behavior.

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    from flaskr.__init__ import create_app
    from flaskr.schema import Users
    from flaskr.schema import Text
    # pass the create_app result so Flask-SQLAlchemy gets the configuration. for the db object, not the app object
    db.create_all(app=create_app())
    click.echo('Initialized the database.')
