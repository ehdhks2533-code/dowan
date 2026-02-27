from flask import Blueprint, request, jsonify
from auth.auth import token_required
from services.log_manager import LogManager

logs_bp = Blueprint('logs', __name__, url_prefix='/api/logs')

@logs_bp.route('/<service_id>', methods=['GET'])
@token_required
def get_logs(auth_payload, service_id):
    """서비스 로그 조회"""
    try:
        limit = request.args.get('limit', 100, type=int)
        logs = LogManager.read_logs(service_id, limit=limit)

        return jsonify({
            'success': True,
            'service_id': service_id,
            'logs': logs,
            'count': len(logs)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@logs_bp.route('/<service_id>/clear', methods=['POST'])
@token_required
def clear_logs(auth_payload, service_id):
    """서비스 로그 초기화"""
    try:
        success = LogManager.clear_logs(service_id)
        if success:
            return jsonify({
                'success': True,
                'message': '로그가 초기화되었습니다'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': '로그를 초기화할 수 없습니다'
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@logs_bp.route('/<service_id>/size', methods=['GET'])
@token_required
def get_log_size(auth_payload, service_id):
    """로그 파일 크기 조회"""
    try:
        size_mb = LogManager.get_log_size(service_id)
        return jsonify({
            'success': True,
            'service_id': service_id,
            'size_mb': round(size_mb, 2)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
