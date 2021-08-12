from flaskr.dbp import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(30), unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Text(db.Model):

    req_id = db.Column(db.String, primary_key=True)
    old_text = db.Column(db.Text)
    new_text = db.Column(db.Text)

    def __init__(self, req_id, old_text, new_text):
        self.req_id = req_id
        self.old_text = old_text
        self.new_text = new_text

