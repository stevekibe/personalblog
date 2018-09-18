from flask import render_template, request, redirect, url_for, abort
from . import main
from .. import db
from ..models import User,BlogCategory,Comments,Blog
from ..forms import BlogForm,CommentForm,BlogcategoryForm
from flask_login import login_required,current_user


@main.route('/')
def index():
    '''
    method to the root page
    ''' 
    blogcategory = BlogCategory.get_blogcategories()

    title = 'Home- Welcome'
    return render_template('index.html', title = title, blogcategories=blogcategory)

@main.route('/blogcategory/new-blog/<int:id>', methods=['GET', 'POST'])
@login_required
def new_blog(id):
    ''' 
    method to form a new blog
    '''
    form = BlogForm()
    blogcategory = BlogCategory.query.filter_by(id=id).first()

    if blogcategory is None:
        abort(404)

    if form.validate_on_submit():
        content = form.content.data
        new_blog= Blog(content=content,blogcategory_id= blogcategory.id,user_id=current_user.id)
        new_blog.save_blog()
        return redirect(url_for('.blogcategory', id=blogcategory.id))

    return render_template('new_blog.html', blog_form=form, blogcategory=blogcategory)

@main.route('/blogcategories/<int:id>')
def blogcategory(id):
    blogcategory = BlogCategory.query.get(id)
    if blogcategory is None:
        abort(404)

    blogs=Blog.get_blogs(id)
    return render_template('category.html', blogs=blogs, blogcategory=blogcategory)

@main.route('/add/blogcategory', methods=['GET','POST'])
@login_required
def new_blogcategory():
    '''
    method for creating new blogcategory
    '''
    form = BlogcategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        new_blogcategory = BlogCategory(name=name)
        new_blogcategory.save_blogcategory()

        return redirect(url_for('.index'))

    title = 'New category'
    return render_template('new_blogcategory.html', blogcategory_form = form,title=title)

@main.route('/view-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def view_blog(id):
    '''
    method to view a blog
    '''
    print(id)
    blogs = Blog.query.get(id)
    
    if blogs is None:                                                                                                                                                                                                                           
        abort(404)
    
    comment = Comments.get_comments(id)
    return render_template('view.html', blogs=blogs, comment=comment, blogcategory_id=id)

@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def post_comment(id):
    '''
    method to post comments
    '''
    form = CommentForm()
    title = ' Comment'
    blogs = Blog.query.filter_by(id=id).first()

    if blogs is None:
         abort(404)

    if form.validate_on_submit():
        opinion = form.opinion.data
        new_comment = Comments(opinion=opinion, user_id=current_user.id, blogs_id=blogs.id)
        new_comment.save_comment()
        return redirect(url_for('.view_blog', id=blogs.id))
   
    return render_template('post-comment.html', comment_form=form, title=title)
