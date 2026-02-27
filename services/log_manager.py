import os
from datetime import datetime
from config import Config

class LogManager:
    """서비스 로그 관리"""

    @staticmethod
    def get_log_path(service_id):
        """서비스의 로그 파일 경로"""
        return os.path.join(Config.LOG_DIR, f'{service_id}.log')

    @staticmethod
    def write_log(service_id, message):
        """로그 작성"""
        log_path = LogManager.get_log_path(service_id)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_path, 'a') as f:
            f.write(f'[{timestamp}] {message}\n')

    @staticmethod
    def read_logs(service_id, limit=100):
        """로그 읽기 (최근 limit개)"""
        log_path = LogManager.get_log_path(service_id)
        if not os.path.exists(log_path):
            return []

        with open(log_path, 'r') as f:
            lines = f.readlines()

        # 최근 limit개만 반환
        return lines[-limit:] if lines else []

    @staticmethod
    def clear_logs(service_id):
        """로그 초기화"""
        log_path = LogManager.get_log_path(service_id)
        if os.path.exists(log_path):
            open(log_path, 'w').close()
            return True
        return False

    @staticmethod
    def get_log_size(service_id):
        """로그 파일 크기 (MB)"""
        log_path = LogManager.get_log_path(service_id)
        if os.path.exists(log_path):
            return os.path.getsize(log_path) / 1024 / 1024
        return 0
