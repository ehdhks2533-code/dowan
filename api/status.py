from flask import Blueprint, jsonify
from auth.auth import token_required
from services.system_monitor import SystemMonitor
from services.process_manager import ProcessManager

status_bp = Blueprint('status', __name__, url_prefix='/api/status')

@status_bp.route('/system', methods=['GET'])
@token_required
def get_system_status(auth_payload):
    """시스템 전체 상태 조회"""
    try:
        stats = SystemMonitor.get_system_stats()
        return jsonify({
            'success': True,
            'system': stats
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@status_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard_status(auth_payload):
    """대시보드 종합 상태 조회"""
    try:
        system_stats = SystemMonitor.get_system_stats()
        services = ProcessManager.get_all_services_status()

        # 실행 중인 서비스 수 계산
        running_count = sum(1 for s in services if s['running'])

        return jsonify({
            'success': True,
            'system': system_stats,
            'services': services,
            'summary': {
                'total_services': len(services),
                'running_services': running_count,
                'stopped_services': len(services) - running_count
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
