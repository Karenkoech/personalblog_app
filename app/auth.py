
from crypt import methods

from flask import Blueprint, render_template,redirect,url_for,flash,request
from .import db 
from .models import User
from flask_login import current_user, login_user,logout_user,login_required
from werkzeug.security import generate_password_hash,check_password_hash


auth=Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
    
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('You are now logged in!',category='success')
                login_user(user,remember=True)

                return redirect(url_for('views.home'))
            else:
                flash('Wrong password!',category='danger')
        else:
            flash('No account found!',category='danger')
                
    return render_template('login.html',user=current_user)

@auth.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':   
        email=request.form.get('email')
        username=request.form.get('username')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        email_exists=User.query.filter_by(email=email).first()
        username_exists=User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email already exists',category='danger')
        elif username_exists:
            flash('Username already exists',category='danger')

        elif password1!=password2:
            flash('Passwords do not match',category='danger')
        elif len(username)<3:
            flash('Username must be at least 3 characters',category='danger')
        elif len(password1)<6:
            flash('Password must be at least 6 characters',category='danger')
        elif len(email)<3:
            flash('Email must be at least 3 characters',category='danger')
        else:
            new_user=User(email=email,username=username,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('You are now registered and can login!',category='success')
            return redirect(url_for('auth.login'))
            
    return render_template('register.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

