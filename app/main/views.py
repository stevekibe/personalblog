from flask import render_template, request, redirect, url_for, abort
from . import main
from .. import db
from ..models import User
from flask_login import login_required,current_user


@main.route('/')
def index():
    '''
    method to the root page
    ''' 
    

    title = 'Home- Welcome'
    return render_template('index.html', title = title,)

@main.route('/category/new-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def new_pitch(id):
    ''' 
    method to form a new pitch
    '''
    form = PitchForm()
    category = PitchCategory.query.filter_by(id=id).first()

    if category is None:
        abort(404)

    if form.validate_on_submit():
        content = form.content.data
        new_pitch= Pitch(content=content,category_id= category.id,user_id=current_user.id)
        new_pitch.save_pitch()
        return redirect(url_for('.category', id=category.id))

    return render_template('new_pitch.html', pitch_form=form, category=category)

@main.route('/categories/<int:id>')
def category(id):
    category = PitchCategory.query.get(id)
    if category is None:
        abort(404)

    pitches=Pitch.get_pitches(id)
    return render_template('category.html', pitches=pitches, category=category)

@main.route('/add/category', methods=['GET','POST'])
@login_required
def new_category():
    '''
    method for creating new category
    '''
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        new_category = PitchCategory(name=name)
        new_category.save_category()

        return redirect(url_for('.index'))

    title = 'New category'
    return render_template('new_category.html', category_form = form,title=title)

@main.route('/view-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def view_pitch(id):
    '''
    method to view a pitch
    '''
    print(id)
    pitches = Pitch.query.get(id)
    
    if pitches is None:                                                                                                                                                                                                                           
        abort(404)
    
    comment = Comments.get_comments(id)
    return render_template('view.html', pitches=pitches, comment=comment, category_id=id)

@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def post_comment(id):
    '''
    method to post comments
    '''
    form = CommentForm()
    title = ' Comment'
    pitches = Pitch.query.filter_by(id=id).first()

    if pitches is None:
         abort(404)

    if form.validate_on_submit():
        opinion = form.opinion.data
        new_comment = Comments(opinion=opinion, user_id=current_user.id, pitches_id=pitches.id)
        new_comment.save_comment()
        return redirect(url_for('.view_pitch', id=pitches.id))
   
    return render_template('post-comment.html', comment_form=form, title=title)
