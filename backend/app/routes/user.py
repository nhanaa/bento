from flask import Blueprint, jsonify, request
from services.user import UserService

user_bp = Blueprint('user_bp', __name__)
user_service = UserService()

# testing
@user_bp.route('/', methods=['GET'])
def default():
    return 'Hello, user!'

@user_bp.route('/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@user_bp.route('/email/<email>', methods=['GET'])
def get_user_by_email(email):
    user = user_service.get_user_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')

    if not email or not name:
        return jsonify({"error": "Email and name are required"}), 400

    user = user_service.create_user(email, name)
    return jsonify(user), 201

@user_bp.route('/<user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    data = request.get_json()
    user = user_service.update_user_by_id(user_id, data)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@user_bp.route('/email/<email>', methods=['PUT'])
def update_user_by_email(email):
    data = request.get_json()
    user = user_service.update_user_by_email(email, data)
    print('User:', user)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    user = user_service.delete_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"})

@user_bp.route('/email/<email>', methods=['DELETE'])
def delete_user_by_email(email):
    user = user_service.delete_user_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"})
