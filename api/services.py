from flask import Blueprint, request, jsonify
from auth.auth import token_required
from services.process_manager import ProcessManager
from services.log_manager import LogManager

services_bp = Blueprint('services', __name__, url_prefix='/api/services')

@services_bp.route('', methods=['GET'])
@token_required
def get_services(auth_payload):
    """모든 서비스 상태 조회"""
    try:
        services = ProcessManager.get_all_services_status()
        return jsonify({
            'success': True,
            'services': services,
            'count': len(services)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@services_bp.route('/<service_id>', methods=['GET'])
@token_required
def get_service(auth_payload, service_id):
    """특정 서비스 상태 조회"""
    try:
        status = ProcessManager.get_service_status(service_id)
        if not status:
            return jsonify({'success': False, 'message': '서비스를 찾을 수 없습니다'}), 404

        # 로그 정보 추가
        log_size = LogManager.get_log_size(service_id)
        status['log_size_mb'] = round(log_size, 2)

        return jsonify({
            'success': True,
            'service': status
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@services_bp.route('/<service_id>/start', methods=['POST'])
@token_required
def start_service(auth_payload, service_id):
    """서비스 시작"""
    try:
        result = ProcessManager.start_service(service_id)
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@services_bp.route('/<service_id>/stop', methods=['POST'])
@token_required
def stop_service(auth_payload, service_id):
    """서비스 중지"""
    try:
        result = ProcessManager.stop_service(service_id)
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@services_bp.route('/<service_id>/restart', methods=['POST'])
@token_required
def restart_service(auth_payload, service_id):
    """서비스 재시작"""
    try:
        result = ProcessManager.restart_service(service_id)
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
