#!/usr/bin/env python3
"""
예제 스크립트 - 대시보드에서 테스트할 수 있는 샘플 서비스
"""

import time
import sys
import random

def main():
    print("예제 스크립트가 시작되었습니다")
    print(f"프로세스 ID: {sys.argv} 시작 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    counter = 0
    try:
        while True:
            counter += 1
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            # 다양한 로그 메시지 출력
            if counter % 5 == 0:
                print(f"[{timestamp}] 작업 진행 중... (반복: {counter})")
            elif counter % 10 == 0:
                print(f"[{timestamp}] 경고: 메모리 사용량 증가 추세")
            elif counter % 20 == 0:
                print(f"[{timestamp}] 성공: 데이터 동기화 완료")
            else:
                print(f"[{timestamp}] 일반 로그: 시스템 정상 작동 중")

            sys.stdout.flush()
            time.sleep(2)

    except KeyboardInterrupt:
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 프로세스가 중단되었습니다")
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 오류 발생: {str(e)}")

if __name__ == '__main__':
    main()
