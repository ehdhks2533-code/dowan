from flask import Blueprint, request, jsonify
from auth.auth import AuthManager

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """로그인 엔드포인트"""
    data = request.get_json()

    if not data or 'password' not in data:
        return jsonify({'message': '비밀번호가 필요합니다'}), 400

    if AuthManager.verify_password(data['password']):
        token = AuthManager.generate_token()
        return jsonify({
            'success': True,
            'token': token,
            'message': '로그인 성공'
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': '비밀번호가 잘못되었습니다'
        }), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """로그아웃 엔드포인트"""
    return jsonify({
        'success': True,
        'message': '로그아웃 되었습니다'
    }), 200

@auth_bp.route('/verify', methods=['GET'])
def verify():
    """토큰 검증 (간단한 검증)"""
    token = None

    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({'valid': False}), 401

    if not token:
        return jsonify({'valid': False}), 401

    payload = AuthManager.verify_token(token)
    if payload:
        return jsonify({'valid': True}), 200
    return jsonify({'valid': False}), 401
