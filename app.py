from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from config import Config
from api import auth_bp, services_bp, logs_bp, status_bp
import os

def create_app():
    """Flask 앱 생성"""
    app = Flask(__name__, static_folder='static', static_url_path='/static')

    # 설정 로드
    app.config.from_object(Config)

    # CORS 설정
    CORS(app, origins=Config.CORS_ORIGINS)

    # API 블루프린트 등록
    app.register_blueprint(auth_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(status_bp)

    # 정적 파일 서빙
    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')

    @app.route('/static/<path:path>')
    def serve_static(path):
        return send_from_directory('static', path)

    # 헬스 체크
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy'}), 200

    # 에러 핸들러
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': '찾을 수 없습니다'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': '내부 서버 오류'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    print(f"Flask 앱 시작: http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
