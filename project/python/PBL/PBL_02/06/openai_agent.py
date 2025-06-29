"""
생성형 AI 활용을 위한 머신러닝 & 딥러닝 6번 문제 - OpenAI 함수 호출 기능 활용 AI Agent 구현

문제 상황
최근 OpenAI의 GPT-4 모델에는 대화 중 함수 호출(Function Calling) 기능이 추가되어, 사용자의 요청을 외부 함수로 처리할 수 있는 구조를 지원하고 있습니다.
이 기능은 계산, 날짜 변환, 검색 등 명확한 작업을 코드 수준에서 처리하고 결과만 대화에 반영할 수 있게 하여, 챗봇의 정확성과 활용도를 크게 높이고 있습니다.
이 기능을 활용하여, 날짜 형식 변환 및 덧셈 요청을 자동으로 처리할 수 있는 AI 에이전트를 구현합니다.
사용자가 자연어로 요청하면 모델이 적절한 함수를 선택하여 호출하고, 그 결과를 다시 자연어로 응답합니다.

문제 정의 및 요구사항
- OpenAI GPT-4 API를 이용하여 함수 기반 AI 비서를 파이썬으로 구현하시오
- 아래 두 개의 사용자 정의 함수를 정의하고 등록하시오:
    - convert_date_format: 날짜 문자열을 다른 형식으로 변환하는 함수
    - add_numbers: 두 숫자를 더하는 함수
- 사용자의 자연어 입력을 기반으로 GPT 모델이 자동으로 적절한 함수를 선택하여 호출하도록 구성하시오.
- 모델의 응답 흐름은 아래와 같아야 한다.
    - 사용자 입력 → 모델이 함수 호출 판단
    - 모델이 호출 요청한 함수 → 직접 실행
    - 실행 결과 → 다시 모델에 전달
    - 최종 자연어 응답 생성
- 구현 조건
    - openai Python 라이브러리 사용
    - OpenAiAgent 클래스를 만들어 기능 구성
    - 함수 호출 여부 판단, 실행 결과 처리 로직 포함
    - 함수 호출 여부 판단, 실행 결과 처리 로직 포함
    - 실제 실행 가능한 코드로 구성할 것(단, API Key는 하드코딩하지 말고 별도 변수 처리)

문제 해결 가이드
- API 환경 설정
    - openai 및 OpenAI 모듈 임포트
    - API Key 변수 설정(실제 실행 시 환경 변수 등 활용 권장)
- 함수 정의
    - convert_date_format(date_str, current_format, target_format)
    - add_numbers(x, y)
    - 두 함수에 대한 Function Calling용 JSON schema 정의
- 에이전트 클래스 구현
    - OpenAIAgent 클래스
    - chat() 메서드: 사용자 입력을 받아 대화 처리
    - call_openai, handle_function_call 등 서브 메서드 포함
- 함수 호출 흐름 처리
    - 모델의 응답에 function_call 존재 시 → 함수 실행
    - 실행 결과를 messages에 추가하여 두 번째 요청 → 최종 자연어 응답
- 테스트
    - "2024-12-25을 '2024년 12월 25일' 형식으로 바꿔줘"
    - "23.5와 3.1을 더하면 얼마야?" 등으로 테스트
"""

import os
import openai
import json
from datetime import datetime

# 환경 변수
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# 함수 정의

# Fuction Calling

# 