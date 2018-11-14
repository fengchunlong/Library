from flask import jsonify, request, url_for
from app import db
from app.models import User
from app.api import api
from app.api.auth import token_auth
from app.api.errors import bad_request

@api.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@api.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@api.route('/users/<int:id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followers, page, per_page,
                                   'api.get_followers', id=id)
    return jsonify(data)


@api.route('/users/<int:id>/followed', methods=['GET'])
@token_auth.login_required
def get_followed(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followed, page, per_page,
                                   'api.get_followed', id=id)
    return jsonify(data)


@api.route('/users', methods=['POST'])
def create_user():
    """
    注册用户
    """
    res = request.values or {}
    if 'truename' not in res or 'phone' not in res or 'password' not in res:
        return bad_request('必须填写真实姓名、手机号和密码')
    if User.query.filter_by(truename=res['truename']).first():
        return bad_request('该用户名已经被注册')
    if User.query.filter_by(phone=res['phone']).first():
        return bad_request('该手机号已被注册')
    user = User(
        truename = res['truename'],
        phone    = res['phone'],
        password = res['password'],
    )
    db.session.add(user)
    db.session.commit()
    # response = jsonify(user.to_dict())
    # response.status_code = 201
    # response.headers['Location'] = url_for('api.get_user', id=user.id)
    response = {}
    response['status'] = 200
    response['message'] = '注册成功'
    return jsonify(response)

@api.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())