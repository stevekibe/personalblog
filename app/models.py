from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from sqlalchemy.sql import func

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User (UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True, index=True)
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    # pitches = db.relationship("Pitch", backref="user", lazy= "dynamic")
    # comment = db.relationship("Comments", backref="user", lazy= "dynamic")
    # vote = db.relationship("Votes", backref="user", lazy= "dynamic")

    
    @property
    def password(self):
        raise AttributeError('You can not read the password Attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User{self.username}'
class BlogCategory(db.Model):
    '''
    the blog category
    '''
    __tablename__ = 'blogcategories'

    id = db.Column(db.Interger, primary_key = True)
    name = db.column(db.string(255))
    description = db.column(db.string(255))
    def save_blogcategory(self):
        '''
        saving the categories
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blogcategories(cls):
        blogcategories = BlogCategory.query.all()
        return blogcategories

    class Blog(db.Model):
        '''
        blog class
        '''
        __tablename__ = 'blogs'

        id = db.Column(db.Integer,primary_key)

