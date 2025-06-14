# --------------------------------------------------------------------------------------------------------------------------------------------

# 생성형 AI 활용을 위한 파이썬 3번 문제 - 디렉터리 감시를 통한 보안 위협 감지

# 문제 상황
# 시스템 보안을 위해 특정 디렉터리에 새로운 파일이 생성되는지 모니터링해야 하며, 보안 위험이 될 수 있는 파일과 내용을 탐지해야 합니다.

# 문제 정의 및 요구사항
# - 디렉터리 : ./monitor_directory
# - 새로운 파일 탐지 및 출력
# - .py, .js, .clss 파일은 주의 파일로 분류
# - 주요 정보 탐지 : 주석, 이메일, SQL문

# --------------------------------------------------------------------------------------------------------------------------------------------

import os
import re
import time

MONITOR_DIR = "monitor_directory"

# 초기 파일 목록 가져오기
def get_file_list():
    # 디렉터리가 존재하지 않으면 새로 생성
    if (os.path.isdir(MONITOR_DIR) == False):
        os.mkdir(MONITOR_DIR)
    
    file_list = set(os.listdir(MONITOR_DIR))
    return file_list

# 위험 확장자 확인하기
def check_dangerous_extension():
    pass

# 민감 정보 탐지
def detect_sensitive_info():
    pass

# 현재 디렉터리 파일 가져오기
initial_files = get_file_list()

# 현재 디렉터리 파일 출력
print(f"현재 디렉토리 : {MONITOR_DIR}/")
for filename in initial_files:
    print(f"├── {filename}")

# 새로운 파일 탐지를 위한 무한 루프
while True:
    # 현재 파일 목록 가져오기
    current_files = get_file_list()

    # 새로운 파일 식별
    new_files = current_files.difference(initial_files)

    if new_files:
        for filename in new_files:
            print(f"├── (new) {filename}")
    
    # 초기 파일 목록 업데이트
    initial_files = current_files
    
    # 일정 시간 대기
    time.sleep(5)