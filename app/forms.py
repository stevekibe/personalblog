from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

class BlogForm(FlaskForm):
    '''
    Class to create a blog
    '''
    content = TextAreaField('YOUR BLOG')
    submit = SubmitField('SUBMIT')

class CommentForm(FlaskForm):
    '''
    Class to create a comment
    '''
    opinion = TextAreaField('WRITE COMMENT')
    submit = SubmitField('SUBMIT')

class BlogcategoryForm(FlaskForm):
    '''
    Class to create a category
    '''
    name =  StringField('Category Name', validators=[Required()])
    submit = SubmitField('Create')