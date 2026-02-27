import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from config import Config

class AuthManager:
    """간단한 토큰 기반 인증 관리"""

    # 토큰 저장소 (실제 프로덕션에서는 DB 사용)
    _valid_tokens = set()

    @staticmethod
    def generate_token(user_id='admin'):
        """토큰 생성 (간단한 해시 기반)"""
        # 무작위 토큰 생성
        token = secrets.token_urlsafe(32)
        AuthManager._valid_tokens.add(token)
        return token

    @staticmethod
    def verify_token(token):
        """토큰 검증"""
        if token in AuthManager._valid_tokens:
            return {'user_id': 'admin'}
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
