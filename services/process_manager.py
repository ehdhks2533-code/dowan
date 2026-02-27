import subprocess
import json
import os
from datetime import datetime
from config import Config, SERVICES
from .log_manager import LogManager
from .system_monitor import SystemMonitor

class ProcessManager:
    """프로세스/서비스 관리"""

    # 실행 중인 프로세스 추적
    _running_processes = {}

    @staticmethod
    def get_service_config(service_id):
        """서비스 설정 조회"""
        return SERVICES.get(service_id)

    @staticmethod
    def start_service(service_id):
        """서비스 시작"""
        service = ProcessManager.get_service_config(service_id)
        if not service:
            return {'success': False, 'message': f'서비스를 찾을 수 없습니다: {service_id}'}

        if service_id in ProcessManager._running_processes:
            pid = ProcessManager._running_processes[service_id]
            if SystemMonitor.process_exists(pid):
                return {'success': False, 'message': '이미 실행 중입니다', 'pid': pid}

        try:
            # 로그 파일 준비
            log_path = LogManager.get_log_path(service_id)

            # 프로세스 시작
            with open(log_path, 'a') as log_file:
                process = subprocess.Popen(
                    service['command'],
                    shell=True,
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    cwd=os.path.dirname(__file__)
                )

            ProcessManager._running_processes[service_id] = process.pid
            LogManager.write_log(service_id, f'프로세스 시작됨 (PID: {process.pid})')

            return {
                'success': True,
                'message': '서비스가 시작되었습니다',
                'pid': process.pid
            }
        except Exception as e:
            LogManager.write_log(service_id, f'시작 실패: {str(e)}')
            return {'success': False, 'message': f'시작 실패: {str(e)}'}

    @staticmethod
    def stop_service(service_id):
        """서비스 중지"""
        if service_id not in ProcessManager._running_processes:
            return {'success': False, 'message': '실행 중인 프로세스가 없습니다'}

        pid = ProcessManager._running_processes[service_id]

        try:
            import signal
            os.kill(pid, signal.SIGTERM)
            del ProcessManager._running_processes[service_id]
            LogManager.write_log(service_id, f'프로세스 중지됨 (PID: {pid})')

            return {
                'success': True,
                'message': '서비스가 중지되었습니다',
                'pid': pid
            }
        except ProcessLookupError:
            del ProcessManager._running_processes[service_id]
            return {'success': True, 'message': '서비스가 이미 중지되었습니다'}
        except Exception as e:
            return {'success': False, 'message': f'중지 실패: {str(e)}'}

    @staticmethod
    def get_service_status(service_id):
        """서비스 상태 조회"""
        service = ProcessManager.get_service_config(service_id)
        if not service:
            return None

        status = {
            'id': service_id,
            'name': service['name'],
            'description': service['description'],
            'enabled': service['enabled'],
            'running': False,
            'pid': None,
            'info': None,
        }

        if service_id in ProcessManager._running_processes:
            pid = ProcessManager._running_processes[service_id]
            if SystemMonitor.process_exists(pid):
                status['running'] = True
                status['pid'] = pid
                status['info'] = SystemMonitor.get_process_info(pid)
            else:
                del ProcessManager._running_processes[service_id]

        return status

    @staticmethod
    def get_all_services_status():
        """모든 서비스 상태 조회"""
        services = []
        for service_id in SERVICES.keys():
            status = ProcessManager.get_service_status(service_id)
            if status:
                services.append(status)
        return services

    @staticmethod
    def restart_service(service_id):
        """서비스 재시작"""
        stop_result = ProcessManager.stop_service(service_id)
        if stop_result['success'] or '실행 중인 프로세스가 없습니다' in stop_result['message']:
            return ProcessManager.start_service(service_id)
        return stop_result
