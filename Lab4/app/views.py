# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, session, redirect, url_for, flash
from app import app
from app.forms import Myform
import os
from loguru import logger
import datetime as dt


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
        receive_form_info(form)
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


@app.context_processor
def footer_info():
    date = dt.datetime.now()
    os_information = [os.name, os.getlogin()]
    return dict(os_information=os_information, user_info=request.headers.get('User-Agent'), date=date)


def receive_form_info(form):
    logger.add("messages.log", format="{time:YYYY-MM-DD HH:mm:ss.SSS} | [{level}] | {message}")
    logger.success(f"{form.name.data} | {form.email.data} | {form.phone.data} | {form.subject.data} | {form.message.data} |")

    session['username'] = form.name.data
    session['email'] = form.email.data
