from application import db


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.TEXT)
    tags = db.Column(db.String)


db.create_all()
