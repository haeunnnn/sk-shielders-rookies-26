# --------------------------------------------------------------------------------------------------------------------------------------------

# 생성형 AI 활용을 위한 파이썬 3번 문제 - 디렉터리 감시를 통한 보안 위협 감지

# 문제 상황
# 시스템 보안을 위해 특정 디렉터리에 새로운 파일이 생성되는지 모니터링해야 하며, 보안 위험이 될 수 있는 파일과 내용을 탐지해야 합니다.

# 문제 정의 및 요구사항
# - 디렉터리 : ./monitor_directory
# - 새로운 파일 탐지 및 출력
# - .py, .js, .class 파일은 주의 파일로 분류
# - 주요 정보 탐지 : 주석, 이메일, SQL문 (정규식 탐지)

# --------------------------------------------------------------------------------------------------------------------------------------------

import os
import re
import time

# 모니터링할 디렉터리 주소
MONITOR_DIR = "./monitor_directory"
# 주의할 파일 확장자
DANGEROUS_EXTENSIONS = {'.py', '.js', '.class'}
# 민감한 정보 정규 표현식
SENSITIVE_PATTERNS_INFO = [
    ("파이썬 주석", r"#.*"),
    ("JS 한 줄 주석", r"//.*"),
    ("JS 여러 줄 주석", r"/\*[\s\S]*?\*/"),
    ("이메일", r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    ("SQL문", r"(?:SELECT|INSERT|UPDATE|DELETE|CREATE\s+TABLE).*?(?:;|$)")
]

# 초기 파일 목록 가져오기
def get_file_list():    
    file_list = set(os.listdir(MONITOR_DIR))
    return file_list

# 위험 확장자 확인하기
def check_dangerous_extension(file):
    is_dangerous = False

    # 파일 이름, 확장자 분리하기
    file_name, extension = os.path.splitext(file)
    # 파일 확장자가 주의 확장자 중 하나일 때
    if extension in DANGEROUS_EXTENSIONS:
        is_dangerous = True
    
    return is_dangerous

# 민감 정보 탐지
def detect_sensitive_info(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            # 파일 전체 내용 읽기
            file_text = f.read()
    except Exception as e:
        print(f"     ! 오류: 파일 {file_path} 읽기 중 오류 발생: {e}")
        return
    
    # 민감 정보를 포함하고 있는지 확인
    for pattern_name, sensitive_pattern in SENSITIVE_PATTERNS_INFO:
        sensitive_infos = re.findall(sensitive_pattern, file_text)
        
        # 민감 정보를 포함하고 있을 때
        if sensitive_infos:
            for sensitive_info in sensitive_infos:
                # 탐지된 민감 정보의 길이를 축약하여 출력
                display_info = (sensitive_info[:70] + '...') if len(sensitive_info) > 70 else sensitive_info
                print(f"     ! 민감 정보가 탐지 ({pattern_name}) : {display_info}")

def main():
    # 디렉터리가 존재하지 않으면 새로 생성
    if (os.path.isdir(MONITOR_DIR) == False):
        os.mkdir(MONITOR_DIR)

    # 현재 디렉터리 파일 가져오기
    initial_files = get_file_list()

    # 현재 디렉터리 파일 출력
    print(f"현재 디렉토리 : {MONITOR_DIR}/")
    for file in initial_files:
        print(f"├── {file}")

    # 새로운 파일 탐지를 위한 무한 루프
    while True:
        # 현재 파일 목록 가져오기
        current_files = get_file_list()

        # 새로운 파일 탐지
        new_files = current_files.difference(initial_files)
        
        # 새로운 파일이 존재할 때
        if new_files:
            for file in new_files:
                file_path = os.path.join(MONITOR_DIR, file)
                # 새로 생성된 것이 파일일 경우
                if os.path.isfile(file_path):
                    # 새로운 파일의 확장자 확인
                    if check_dangerous_extension(file):
                        print(f"├── (new) {file} → 주의")
                    else:
                        print(f"├── (new) {file}")
                    
                    # 새로운 파일의 내용 확인
                    detect_sensitive_info(file_path)

                # 새로 생성된 것이 디렉토리일 경우
                else:
                        print(f"├── (new) {file}")
        
        # 초기 파일 목록 업데이트
        initial_files = current_files
        
        # 일정 시간 대기
        time.sleep(5)

if __name__ == "__main__":
    main()