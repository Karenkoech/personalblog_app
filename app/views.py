
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user,login_required
from .models import Comment, Post, User, Vote
from . import db

views=Blueprint('views',__name__)

@views.route('/')
@views.route('/home')
def home():
    posts=Post.query.all()

    return render_template('home.html',user= current_user,posts=posts)

@views.route('/dashboard')
def dashboard():
    posts=Post.query.all()

    return render_template('dashboard.html',user= current_user,posts=posts)

@views.route('/create_post',methods=['GET','POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')
        
        if not text:
            flash('Please fill in all fields',category='danger')
            
        else:
            post = Post(text=text,author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created successfully!', category='success')
            return redirect(url_for('views.home'))
    return render_template('create_post.html',user= current_user)

@views.route('/delete_post/<id>')
@login_required
def delete_post(id):
    post=Post.query.filter_by(id=id).first()
    if not post:
        flash('Post not found',category='danger')

    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', category='success')

    return redirect(url_for('views.home'))

@views.route('/posts/<username>')
@login_required
def posts(username):
    user=User.query.filter_by(username=username).first()
    if not user:
        flash('User not found',category='danger')
        return redirect(url_for('views.home'))
        
    posts=user.posts
    return render_template('posts.html',user=current_user,posts=posts,username=username)

@views.route('/create_comment/<post_id>',methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Please fill in all fields',category='danger')

    else:
        post=Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text,author=current_user.id,post_id=post_id)
            db.session.add(comment)
            db.session.commit()   
        else:
            flash('Post not found',category='danger')
            
    return redirect(url_for('views.home'))
    
@views.route('/delete_comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    comment=Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment not found',category='danger')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment',category='danger')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))

@views.route('/vote_post/<post_id>',methods=['GET'])
@login_required
def vote_post(post_id):
    post=Post.query.filter_by(id=post_id).first()
    vote=Vote.query.filter_by(post_id=post_id,author=current_user.id).first()

    if not post:
        flash('Post not found',category='danger')
    elif vote:
        db.session.delete(vote)
        db.session.commit()
    else:
        vote=Vote(post_id=post_id,author=current_user.id)
        db.session.add(vote)
        db.session.commit()
    return redirect(url_for('views.home'))



