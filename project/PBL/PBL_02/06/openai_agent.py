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
    - 실제 실행 가능한 코드로 구성할 것(단, API Key는 하드코딩하지 말고 별도 변수 처리)
"""

import os
import openai
import json
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# 환경 변수에서 OpenAI API 키 로드
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------------------------------
# 함수 정의
# ---------------------------------------

# 날짜 문자열을 다른 형식으로 변환하는 함수
def convert_date_format(date_str, current_format, target_format):
    try:
        dt = datetime.strptime(date_str, current_format)
        return dt.strftime(target_format)
    except Exception as e:
        return f"날자 변환 오류: {e}"

# 두 숫자를 더하는 함수
def add_numbers(x, y):
    return x + y

# ---------------------------------------
# Function Calling용 함수 정의
# ---------------------------------------

tools = [
    {   
        "type": "function",
        "function": {
            "name": "convert_date_format",
            "description": "날짜 문자열을 지정된 형식으로 변환한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_str": {
                        "type": "string",
                        "description": "입력 날짜 문자열"
                    },
                    "current_format": {
                        "type": "string",
                        "description": "현재 날짜 형식 (예: '%Y-%m-%d')"
                    },
                    "target_format": {
                        "type": "string",
                        "description": "변환할 목표 날짜 형식 (예: '%Y년 %m월 %d일')"
                    }
                },
                "required": ["date_str", "current_format", "target_format"]
            },
        },
    },
    {   
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "두 숫자를 더한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "number",
                        "description": "첫 번째 숫자"
                    },
                    "y": {
                        "type": "number",
                        "description": "두 번째 숫자"
                    }
                },
                "required": ["x", "y"]
            },
        },
    },
]

# ---------------------------------------
# OpenAIAgent 클래스 구현
# ---------------------------------------

class OpenAIAgent:
    def __init__(self, model="gpt-4.1"):
        # 모델명과 대화 메시지 초기화
        self.model = model
        self.messages = [
            {
                "role": "system", 
                "content": "당신은 유능한 AI 비서입니다. 사용자의 요청에 따라 적절한 함수를 호출하고 결과를 자연어로 응답합니다."
            }
        ]
    def chat(self, user_input):
        # 사용자 입력 메시지 추가
        self.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # 1차 OpenAI API 호출
        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message
        tool_call = message.tool_calls[0] if message.tool_calls else None

        # 도구 호출이 있는 경우
        if tool_call:
            function_name = tool_call.function.name
            arguments = tool_call.function.arguments
            arguments = json.loads(arguments)
            
            # 실제 함수 실행
            result = self.call_openai(function_name, arguments)

            # 함수 호출 메시지 및 결과 메시지 추가
            self.messages.append({
                "role": "assistant",
                "tool_calls": [tool_call.model_dump()],
            })

            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(result)
            })

            # 2c차 OpenAI API 호출
            final_response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=tools,
                tool_choice="auto"
            )
            reply = final_response.choices[0].message.content
        else:
            # 도구 호출이 없는 경우, 모델의 응답을 바로 사용
            reply = message.content
        
        # 최종 응답 메시지 추가
        self.messages.append({
            "role": "assistant",
            "content": reply
        })

        return reply
    
    def call_openai(self, function_name, arguments):
        # 함수명에 따라 실제 파이썬 함수 실행
        if function_name =='convert_date_format':
            date_str = arguments.get('date_str')
            current_format = arguments.get('current_format')
            target_format = arguments.get('target_format')
            return convert_date_format(date_str, current_format, target_format)
        
        elif function_name == 'add_numbers':
            x = arguments.get('x')
            y = arguments.get('y')
            return add_numbers(x, y)
        
        else:
            return f"알 수 없는 함수 호출: {function_name}"

# ---------------------------------------
# 테스트 코드
# ---------------------------------------

if __name__ == "__main__":
    agent = OpenAIAgent()

    while True:
        user_input = input("사용자 입력: ")
        if user_input.lower() in ["exit", "quit"]:
            print("프로그램을 종료합니다.")
            break

        response = agent.chat(user_input)
        print(f"응답: {response}")