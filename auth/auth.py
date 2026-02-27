import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from config import Config

class AuthManager:
    """JWT Token 기반 인증 관리"""

    @staticmethod
    def generate_token(user_id='admin'):
        """토큰 생성"""
        payload = {
            'user_id': user_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
        }
        token = jwt.encode(
            payload,
            Config.JWT_SECRET_KEY,
            algorithm='HS256'
        )
        return token

    @staticmethod
    def verify_token(token):
        """토큰 검증"""
        try:
            payload = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def verify_password(password):
        """비밀번호 검증"""
        return password == Config.DEFAULT_PASSWORD

def token_required(f):
    """토큰 검증 데코레이터"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 헤더에서 토큰 추출
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': '유효하지 않은 토큰 형식'}), 401

        if not token:
            return jsonify({'message': '토큰이 필요합니다'}), 401

        payload = AuthManager.verify_token(token)
        if not payload:
            return jsonify({'message': '유효하지 않은 또는 만료된 토큰'}), 401

        return f(payload, *args, **kwargs)

    return decorated
