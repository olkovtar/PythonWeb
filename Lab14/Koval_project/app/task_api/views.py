from flask_restful import Resource, reqparse, fields, marshal_with
from flask import jsonify
from . import task_api_bp, api
from ..task_actions.models import Task, Progress, Priority
from ..import db

task_args = reqparse.RequestParser()
task_args.add_argument('title', type=str)
task_args.add_argument('description', type=str)
task_args.add_argument('progress', type=str)
task_args.add_argument('priority', type=str)
task_args.add_argument('category_id', type=int)
task_args.add_argument('owner_id', type=int)

resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'created': fields.String,
    'progress': fields.String,
    'priority': fields.String,
    'category_id': fields.Integer,
    'owner_id': fields.Integer
}


class TaskApi(Resource):
    @marshal_with(resource_fields)
    def get(self, task_id=None):

        if task_id is None:
            tasks = Task.query.all()
            return tasks

        task = Task.query.get_or_404(task_id)
        return task, 201

    # http://127.0.0.1:5000/api/v2/ for not to catch "without trainling slash" error
    @marshal_with(resource_fields)
    def post(self):
        args = task_args.parse_args()

        title = args['title']
        description = args['description']
        progress = Progress(int(args['progress']))
        priority = Priority(int(args['priority']))
        category_id = args['category_id']
        owner_id = args.get('owner_id')

        new_task = Task(title=title,
                        description=description,
                        priority=priority,
                        progress=progress,
                        category_id=category_id,
                        owner_id=owner_id)

        db.session.add(new_task)
        db.session.commit()

        task = Task.query.filter_by(title=title).first()
        return task, 201

    @marshal_with(resource_fields)
    def put(self, task_id):
        args = task_args.parse_args()

        task = Task.query.get_or_404(task_id)

        if 'title' in args:
            task.title = args['title']

        if 'description' in args:
            task.description = args['description']

        if 'progress' in args:
            task.progress = Progress(int(args['progress']))

        if 'priority' in args:
            task.priority = Priority(int(args['priority']))

        if 'category_id' in args:
            task.category_id = args['category_id']

        if 'owner_id' in args:
            task.owner_id = args['owner_id']

        db.session.commit()
        task = Task.query.get_or_404(task_id)
        return task

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        task_title = task.title

        try:
            db.session.delete(task)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({'message': 'Error while deleting!'})

        return jsonify({'message': f'The task {task_title} has been successfully deleted!'})


api.add_resource(TaskApi, '/<string:task_id>', '/')
