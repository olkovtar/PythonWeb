from flask import jsonify, request, make_response
from flask_jwt_extended import create_access_token, jwt_required
from functools import wraps
from sqlalchemy.exc import IntegrityError

from . import category_api_bp
from ..import db
from ..task_actions.models import Category
from ..account.models import User


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'ole@gmail.com' and auth.password == 'qwerty':
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403
    return decorated


# POST  api/token - get token
@category_api_bp.route('/token', methods=['POST'])
@protected
def get_token():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login required!"'})

    if user.verify_password(auth.password):
        token = create_access_token(identity=user.email)
        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login required!"'})


# GET  api/entities - get list of entities
@category_api_bp.route('/category', methods=['GET'])
@jwt_required()
def get_categories():

    categories = Category.query.all()

    categories_list = [dict(id=category.id, name=category.name) for category in categories]

    return jsonify({'category': categories_list})


# POST / entities - create an entity
@category_api_bp.route('/category', methods=['POST'])
@jwt_required()
def add_category():
    new_category_data = request.get_json()  # {'name': 'pub'}

    if not new_category_data:
        return {'message': 'No input data provided'}, 400

    name = new_category_data.get('name')
    if not name:
        return jsonify({'message': 'Not key with name'}), 422

    category = Category.query.filter_by(name=name).first()

    if category:
        return jsonify({'message': f'Категорія з назвою {name} уже існує'}), 400

    try:
        category_new = Category(name=name)
        db.session.add(category_new)
        db.session.commit()
    except:
        return jsonify({'message': f'Невідома помилка на стороні сервера'}), 400

    category_add = Category.query.filter_by(name=name).first()

    return jsonify({'message': 'Категорія успішно створена: ', 'id': category_add.id, 'name': category_add.name}), 201


# GET /entities/<entity_id> - get entity information
@category_api_bp.route('/category/<int:id>', methods=['GET'])  # api/category/4
@jwt_required()
def get_category(id):
    category = Category.query.get_or_404(id)

    return jsonify(dict(id=category.id, name=category.name))


# PUT / entities/<entity_id> - update entity
@category_api_bp.route('/category/<int:id>', methods=['PUT'])
@jwt_required()
def edit_category(id):

    new_category_data = request.get_json()

    name = new_category_data.get('name')  # {'name': 'pub'}
    if not name:
        # Якщо в json даних назва ключа != "name"
        return jsonify({'message': 'Not key with this name'})

    category = Category.query.get_or_404(id)
    old_name = category.name
    try:
        category.name = name  # Модель Сategory має унікальне поле name
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Така категорія уже існує'})
        # return jsonify({'message': 'Така категорія уже існує'}), 409

    # return jsonify({'message': 'Категорія успішно оновлена', 'id': id, 'name': name}), 204
    return jsonify({'message': f'Категорія з назвою "{old_name}" успішно змінена на "{name}"'})


# DELETE / entities/<entity_id> - delete entity
@category_api_bp.route('/category/<int:id>', methods=['DELETE'])
@jwt_required()
# @protected
def delete_category(id):
    category = Category.query.get_or_404(id)
    category_name = category.name
    try:
        db.session.delete(category)
        db.session.commit()
    except:
        return jsonify({'message': f'Невідома помилка на стороні сервера'}), 500

    # return jsonify({'message': f'Категорія {category_name} успішно видалена'}), 204
    return jsonify({'message': f'Категорія "{category_name}" успішно видалена'})
