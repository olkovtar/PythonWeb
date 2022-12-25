from flask import Blueprint

task_actions_bp = Blueprint('task_actions', __name__,
                            template_folder='templates/task_actions')
from . import views