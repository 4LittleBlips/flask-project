from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, CreatePostForm, AddCommentForm, AddReplyForm, EditCommentForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Comment
from werkzeug.urls import url_parse
from datetime import datetime


@app.context_processor
def inject_user():
    users = User.query.all()
    users = tuple(users)
    return dict(users=users)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')
    
        if next_page == None or url_parse(next_page).netloc != '':
                next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])

def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! You are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)
    return render_template('profile.html', user=user, posts=posts)



@app.route('/user/<username>/edit-profile', methods=['GET', 'POST'])
@login_required
def editProfile(username):
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('profile', username=username))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title='Edit Your Profile', form=form)





@app.route('/user/<username>/post', methods=['GET', 'POST'])
@login_required
def createPost(username):
    form = CreatePostForm()
    
    if form.validate_on_submit():
        p = Post(body=form.text.data, author=current_user)
        db.session.add(p)
        db.session.commit()
        flash('You have successfully created your post!')
        return redirect(url_for('profile', username=username))

    elif request.method == 'GET': 
        return render_template('create_post.html', title='Create A Post', form=form)



@app.route('/posts/<int:post_id>', methods=['GET', 'POST'])
def showPost(post_id):
    post = Post.query.get(post_id)
    commentForm = AddCommentForm()
    replyForm = AddReplyForm()
    editForm = EditCommentForm()
    
    if commentForm.validate_on_submit():
        c = Comment(body=commentForm.text.data, post=post, commenter=current_user)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('showPost', title=post.title, post_id=post.id, commentForm=commentForm, replyForm=replyForm, editForm=editForm))

    return render_template('show_post.html', post=post, commentForm=commentForm, replyForm=replyForm, editForm=editForm)


@app.route('/posts/<int:post_id>/<int:comment_id>', methods=['POST'])
def addReply(post_id, comment_id):
    replyForm = AddReplyForm()
    post = Post.query.get(post_id) 
    if replyForm.validate_on_submit():

        c = Comment.query.get(comment_id)
        r = Comment(body=replyForm.text.data, commenter=current_user, parent=c)
        db.session.add(r)
        db.session.commit()
    return redirect(url_for('showPost', title=post.title, post_id=post_id))


@app.route('/posts/<int:comment_id>', methods=['DELETE'])
def deleteComment(comment_id):
    comment = request.args.get('comment_id')
    Comment.query.filter_by(id=comment_id).delete()
    db.session.commit()
    flash('You deleted one of your comments')
    return jsonify(status='success')

@app.route('/comments/<int:comment_id>', methods=['POST'])
def editComment(comment_id):
    comment = request.args.get('comment_id')
    c = Comment.query.get(comment_id)
    c.body = 'Edited2'
    db.session.commit()
    flash('You edited your comment')
    return jsonify(status='succes', edited_id=comment_id, edited_text=c.body)
