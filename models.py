"""Models for Blogly"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

default_img = 'https://www.pngwing.com/en/free-png-augve'

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """User"""
    __tablename__ = "users"
    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default = default_img)

    def __init__(self, first_name, last_name, image_url=None):
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<User {self.full_name()}>"
    



    
    
