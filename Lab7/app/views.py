# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, session, redirect, url_for, flash
from app import app, db
from app.models import Message, User
from app.forms import Myform, RegistrationForm, LoginForm
# import os
from loguru import logger
import datetime as dt

logger.add("messages.log", format="{time:YYYY-MM-DD HH:mm:ss.SSS} | [{level}] | {message}")


@app.route('/')
def about():
    date = dt.datetime.now()
    return render_template('index.html', name='Oleh Koval')


@app.route('/education')
def education():
    date = dt.datetime.now()
    return render_template('education.html')


@app.route('/skills')
def skills():
    date = dt.datetime.now()
    return render_template('skills.html')


# Redirect
@app.route('/home')
def home():
    return redirect(url_for('about'))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = Myform()
    if form.validate_on_submit():
        session['username'] = form.name.data
        session['email'] = form.email.data
        save_message_to_db(form)
        flash(f"Your message has been sent: {form.name.data}, {form.email.data}", category='success')
        return redirect(url_for("contact"))

    elif request.method == 'POST':
        flash("Post method validation failed", category='warning')
        return render_template('contact.html', form=form)

    form.name.data = session.get("username")
    form.email.data = session.get("email")
    return render_template('contact.html', form=form, username=session.get('username'))


@app.route('/clear')
def clear():
    session.pop('username', default=None)
    session.pop('email', default=None)
    return redirect(url_for("contact"))


@app.route('/database')
def database():
    messages = Message.query.all()
    return render_template('database.html', messages=messages)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Account created for {form.username.data}!", category='success')
        except:
            db.session.flush()
            db.session.rollback()

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            return redirect(url_for("home"))
        else:
            flash(f"Login unsuccessful. Email or password is incorrect!", category='danger')
    return render_template('login.html', form=form)


@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', all_users=all_users)


@app.route('/users/delete/<id>')
def delete_user(id):
    db.session.delete(User.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for("users"))


@app.route('/database/delete/<id>')
def delete_message(id):
    db.session.delete(Message.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for("database"))


'''
def footer_info():
    date = dt.datetime.now()
    os_information = [os.name, os.getlogin()]
    return dict(os_information=os_information, user_info=request.headers.get('User-Agent'), date=date)
'''


def save_message_to_db(form):
    logger.success(f"{form.name.data} | {form.email.data} | {form.phone.data} | {form.library.data} | {form.message.data} |")
    session['username'] = form.name.data
    session['email'] = form.email.data

    message = Message(
        name=form.name.data,
        email=form.email.data,
        phone=form.phone.data,
        library=form.library.data,
        message=form.message.data
    )
    try:
        db.session.add(message)
        db.session.commit()
    except:
        db.session.flush()
        db.session.rollback()
