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
    blog = db.relationship("Blog", backref="user", lazy= "dynamic")
    comment = db.relationship("Comments", backref="user", lazy= "dynamic")
    

    
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

        id = db.Column(db.Integer,primary_key= True)
        content = db.Column(db.String)
        blogcategory_id = db.Column(db.Integer, db.ForeignKey("blogcategories.id"))
        user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
        comment = db.relationship("Comments", backref="blogs", lazy= "dynamic")
        

    def save_blog(self):
        '''
        method for saving a pitch
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_blogs(cls):
        Blog.all_blogs.clear()

    def get_blogs(id):
        '''
        method for displaying pitches
        '''
        blogs = Blog.query.filter_by(category_id=id).all()
        return blogs

class Comments(db.Model):
    '''
    class for comments
    '''
    __tablename__= 'comments'

    id = db.Column(db.Integer, primary_key = True)
    opinion = db.Column(db.String(255))
    time_posted = db.Column(db.DateTime, default= datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blogs_id = db.Column(db.Integer, db.ForeignKey("blogs.id"))

    def save_comment(self):
        '''
        method for saving a comment
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comments.query.order_by(
            Comments.time_posted.desc()).filter_by(pitches_id=id).all()
    
        return comment
    
