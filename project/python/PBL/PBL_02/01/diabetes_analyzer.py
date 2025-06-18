"""
생성형 AI 활용을 위한 머신러닝 & 딥러닝 1번 문제 - 당뇨병 진단 데이터를 활용한 데이터 전처리 및 EDA 분석

문제 상황
당뇨병 진단 데이터를 기반으로 기초적인 데이터 전처리 및 탐색적 테이터 분석(EDA)을 수행하는 과제가 주어졌습니다.

문제 정의 및 요구사항
- 데이터셋: diabetes.csv(Pima Indians Diabetes Dataset)
- 결측치 처리: Glucose, BloodPressure, SkinThickness, Insulin, BMI 열에서 0을 결측치로 간주하고 평균으로 대체
- 이상치 처리: SkinThickness, Insulin 열에서 상위 1%를 이상치로 간주하고 평균으로 대체
- 정규화: Age 열을 MinMaxScaler로 0~1 범위로 정규화
- EDA:
    - 각 열의 결측치 개수 출력
    - Outcome 별 Glucose 평균 출력
    - 전처리 후 데이터 프레임 상위 5개 행 출력
"""

