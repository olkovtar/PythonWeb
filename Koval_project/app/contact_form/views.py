from flask import Flask, render_template, request, session, redirect, url_for, flash
from loguru import logger
from .. import db
from .models import Message
from .forms import Myform
from . import contact_form_bp

logger.add("messages.log", format="{time:YYYY-MM-DD HH:mm:ss.SSS} | [{level}] | {message}")


@contact_form_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = Myform()
    if form.validate_on_submit():
        session['username'] = form.name.data
        session['email'] = form.email.data
        save_message_to_db(form)
        flash(f"Your message has been sent: {form.name.data}, {form.email.data}", category='success')
        return redirect(url_for("contact_form.contact"))

    elif request.method == 'POST':
        flash("Post method validation failed", category='warning')
        return render_template('contact.html', form=form)

    form.name.data = session.get("username")
    form.email.data = session.get("email")
    return render_template('contact.html', form=form, username=session.get('username'))


@contact_form_bp.route('/clear')
def clear():
    session.pop('username', default=None)
    session.pop('email', default=None)
    return redirect(url_for("contact_form.contact"))


@contact_form_bp.route('/database')
def database():
    messages = Message.query.all()
    return render_template('database.html', messages=messages)


@contact_form_bp.route('/database/delete/<id>')
def delete_message(id):
    db.session.delete(Message.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for("contact_form.database"))


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

