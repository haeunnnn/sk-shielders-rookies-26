# --------------------------------------------------------------------------------------------------------------------------------------------

# 생성형 AI 활용을 위한 파이썬 2번 문제 - 로그 파일을 활용한 IP 접속 분석

# 문제 상황
# 서버 보안 분석을 위해 로그 파일에서 접속한 IP 주소를 파악해야 하며, 이를 통해 자주 접속한 IP를 분석하고 보고해야 합니다.

# 문제 정의 및 요구사항
# - 사용자 입력 : 로그 파일 경로
# - IP 주소 추출 및 빈도 계산
# - 상위 3개 IP 주소 출력
# - 분석 결과 CSV 저장
#    - 파일명 : ip_analysis.csv

# --------------------------------------------------------------------------------------------------------------------------------------------

import re
import csv

# 로그 파일 경로 입력 받아 파일 읽기
def read_log_file():
    log_lines = []

    file_path = input("로그 파일 경로를 입력해주세요: ")
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in f:
            log_lines.append(line.strip())
    return log_lines

# IP 주소 추출
def extract_ip_addresses(log_lines):
    # IP 주소들을 저장할 리스트
    ip_addresses = []

    # IP 주소 정규 표현식
    ip_pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    
    # 로그 파일 내 IP 주소를 추출하여 리스트에 저장
    for i in log_lines:
        ip_adress = ip_pattern.findall(i)[0]
        ip_addresses.append(ip_adress)
    
    return ip_addresses

# IP 빈도 계산
def calculate_ip_frequency(ip_addresses):
    # IP 주소 별 빈도들을 저장할 딕셔너리
    ip_frequency = {}

    # IP 주소를 저장한 리스트 내 IP 주소들을 순회하며 개수 카운트
    for i in ip_addresses:
        if i in ip_frequency.keys():
            ip_frequency[i] += 1
        else:
            ip_frequency[i] = 1

    # 빈도 수를 기준으로 내림차순 정렬
    sorted_ip_frequency = list(ip_frequency.items())
    sorted_ip_frequency = sorted(sorted_ip_frequency, key = lambda freq: freq[1], reverse=True)

    return sorted_ip_frequency

# 상위 3개 IP 주소 출력
def display_top_3_ips(ip_frequency):
    top_3_ips = ip_frequency[:3]
    print("--------- IP 주소 빈도 상위 3개 출력 ---------")
    for i in top_3_ips:
        print(f"IP 주소 : {i[0]}, 접속 횟수 : {i[1]}")
    print("----------------------------------------------")

# 분석 결과 CSV 저장
def save_analysis_to_csv(ip_frequency):
    for i in ip_frequency:
        print(i)
    # print(ip_frequency)


log_lines = read_log_file()
ip_addresses = extract_ip_addresses(log_lines)
ip_frequency = calculate_ip_frequency(ip_addresses)
display_top_3_ips(ip_frequency)
save_analysis_to_csv(ip_frequency)