from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from .. import db
from .models import Task, Category, Comment
from ..account.models import User
from .forms import Taskform, CategoryForm, CommentForm, AssignUserForm

from . import task_actions_bp


@task_actions_bp.route('/task/create', methods=['GET', 'POST'])
@login_required
def task_create():
    form = Taskform()

    if form.validate_on_submit():

        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data
        priority = form.priority.data
        progress = form.progress.data
        category = form.category.data
        task_info = Task(title=title,
                         description=description,
                         deadline=deadline,
                         priority=priority,
                         progress=progress,
                         category_id=category,
                         owner=current_user)
        task_info.users.append(current_user)
        db.session.add(task_info)
        db.session.commit()

        flash(f"Task created: {form.title.data}", category='success')
        return redirect(url_for("task_actions.task_create"))

    elif request.method == 'POST':
        flash("Не пройшла валідація з Post", category='warning')
        return redirect(url_for("task_actions.task_create"))

    return render_template('create_task.html', form=form)


@task_actions_bp.route('/task', methods=['GET'])
@login_required
def tasks():
    all_tasks = Task.query.all()
    count = Task.query.count()

    tasks_to_show = Task.query.order_by(Task.priority.desc(),
                                        Task.deadline.asc()).all()
    return render_template('tasks.html',
                           tasks=tasks_to_show,
                           all_tasks=all_tasks,
                           count=count)


@task_actions_bp.route('/task/<int:id>', methods=['GET', 'POST'])
@login_required
def task(id):
    task = Task.query.filter_by(id=id).first()
    task_detail = {
        'Title': task.title,
        'Description': task.description,
        'Created': task.created,
        'Modified': task.modified,
        'Deadline': task.deadline.date(),
        'Progress': task.progress,
        'Priority': task.priority

    }
    form = Taskform()
    form_comment = CommentForm()
    comments = Comment.query.filter_by(task_id=id).all()
    data = {
        'form_comment': form_comment,
        'comments': comments
    }
    return render_template('task.html', task_detail=task_detail,
                           id=task.id,
                           form=form,
                           assigned=task.users,
                           data=data,
                           user=current_user)


@task_actions_bp.route('/task/<int:id>/update', methods=['GET', 'POST'])
@login_required
def task_update(id):

    task = current_user.tasks.filter_by(id=id).first()
    if not task:
        flash("You cannot update this task", category='warning')
        return redirect(url_for("task_actions.task", id=id))

    form = Taskform()
    if form.validate_on_submit():

        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data
        priority = form.priority.data
        progress = form.progress.data

        task.title = title
        task.description = description
        task.deadline = deadline
        task.priority = priority
        task.progress = progress
        db.session.add(task)
        db.session.commit()

        flash(f"Task successfully updated", category='success')
        return redirect(url_for("task_actions.task", id=id))

    elif request.method == 'POST':
        print(form.errors, form.description.data)
        flash("Не пройшла валідація з Post", category='warning')
        return redirect(url_for("task_actions.task", id=id))

    return render_template('update_task.html', title="Update task", form=form, task_id=id)


@task_actions_bp.route('/task/<int:id>/delete', methods=['GET'])
@login_required
def task_delete(id):

    task = current_user.tasks.filter_by(id=id).first()
    if not task:
        flash("You cannot delete this task", category='warning')
        return redirect(url_for("task_actions.task", id=id))

    task_to_del = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_del)
    except:
        db.session.rollback()
    else:
        db.session.commit()
        flash("Task deleted", category='success')
        current_app.logger.info("Task deleted")

    return redirect(url_for('task_actions.tasks'))


@task_actions_bp.route('/categories', methods=['GET'])
@login_required
def categories():
    count = Task.query.count()
    categories_to_show = Category.query.all()
    return render_template('categories.html',
                           categories=categories_to_show,
                           count=count)


@task_actions_bp.route('/category/create', methods=['GET', 'POST'])
@login_required
def category_add():
    form = CategoryForm()
    title = "Add Category"
    if form.validate_on_submit():
        if current_user.is_authenticated:
            category = Category(name=form.name.data)

            try:
                db.session.add(category)
            except:
                db.session.rollback()
            else:
                db.session.commit()
                flash("Category added", category='success')
        else:
            return redirect(url_for('account.login'))

    if request.method == 'POST':
        return redirect(url_for('task_actions.categories'))

    return render_template('category_form.html', form=form, title=title)


@task_actions_bp.route('/category/<int:id>/update', methods=['GET', 'POST'])
@login_required
def category_update(id):
    category_to_update = Category.query.get_or_404(id)
    title = "Update Category"
    form = CategoryForm(name=category_to_update.name)

    if form.validate_on_submit():

        if current_user.is_authenticated:
            try:
                category_to_update.name = form.name.data
            except:
                db.session.rollback()
            else:
                db.session.commit()
                flash("Category updated", category='success')
                current_app.logger.info("Category updated")
        else:
            return redirect(url_for('account.login'))

    if request.method == 'POST':
        return redirect(url_for('task_actions.categories', id=category_to_update.id))

    return render_template('category_form.html', form=form, title=title)


@task_actions_bp.route('/categories/<int:id>/delete', methods=['GET'])
@login_required
def category_delete(id):
    category_ = Category.query.get_or_404(id)

    try:
        db.session.delete(category_)
    except:
        db.session.rollback()
    else:
        db.session.commit()
        flash("Category deleted", category='success')
        current_app.logger.info("Category deleted")

    return redirect(url_for('task_actions.categories'))


@task_actions_bp.route('/task/add_comment/<int:task_id>', methods=['GET', 'POST'])
@login_required
def add_comment(task_id):
    task = current_user.tasks.filter_by(id=task_id).first()
    if not task:
        flash("You cannot add comment to this task", category='warning')
        return redirect(url_for("task_actions.task", id=task_id))
    form = CommentForm()
    if form.validate_on_submit():
        text = form.text.data
        comment = Comment(content=text,
                          task_id=task_id)
        db.session.add(comment)
        db.session.commit()

        flash(f"Comment successfully added", category='success')
        return redirect(url_for("task_actions.task", id=task_id))

    elif request.method == 'POST':
        flash("Не пройшла валідація з Post", category='warning')

    return render_template('comment_form.html', title="Task", task_id=task_id, form=form)


@task_actions_bp.route('/task/<int:task_id>/assign/user', methods=['GET', 'POST'])
@login_required
def assign_user_task(task_id):

    task = Task.query.filter_by(id=task_id).first()
    if task.owner_id != current_user.id:
        flash("You cannot assign users to this task", category='warning')
        return redirect(url_for("task_actions.task", id=task_id))

    form = AssignUserForm()
    if form.validate_on_submit():
        if not form.email.data:
            flash("Fill the email field", category='warning')
            return redirect(url_for("task_actions.task", id=task_id))
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("No user with such email", category='warning')
            return redirect(url_for("task_actions.task", id=task_id))
        task.users.append(user)
        db.session.add(task)
        db.session.commit()
        flash("Successfully assigned user", category='success')

    elif request.method == 'POST':
        flash("Не пройшла валідація з Post", category='warning')
        return redirect(url_for("task_actions.assign_user_task", id=task_id))

    return render_template('assign_user.html', id=task_id, form=form)


@task_actions_bp.route('/user/profile/<int:user_id>')
@login_required
def user_profile(user_id):
    user_info = User.query.filter_by(id=user_id).first()
    task_list = user_info.tasks
    return render_template('user.html', user_info=user_info, task_list=task_list)
