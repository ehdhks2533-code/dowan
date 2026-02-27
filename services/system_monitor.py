import psutil
import os
from datetime import datetime

class SystemMonitor:
    """시스템 프로세스 모니터링"""

    @staticmethod
    def get_process_info(pid):
        """프로세스 정보 조회"""
        try:
            process = psutil.Process(pid)
            return {
                'pid': pid,
                'name': process.name(),
                'status': process.status(),
                'cpu_percent': process.cpu_percent(interval=0.1),
                'memory_mb': process.memory_info().rss / 1024 / 1024,
                'create_time': datetime.fromtimestamp(process.create_time()).isoformat(),
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    @staticmethod
    def get_process_by_name(name):
        """이름으로 프로세스 찾기"""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if name.lower() in proc.info['name'].lower():
                    return proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    @staticmethod
    def process_exists(pid):
        """프로세스 존재 여부 확인"""
        try:
            psutil.Process(pid)
            return True
        except psutil.NoSuchProcess:
            return False

    @staticmethod
    def get_system_stats():
        """시스템 전체 통계"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
        }
