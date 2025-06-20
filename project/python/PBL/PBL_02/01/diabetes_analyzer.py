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

# 필요한 라이브러리 임포트
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기
df = pd.read_csv('diabetes.csv')

# 결측치 처리할 열 리스트로 저장
columns_to_replace = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

# ------ 결측치 처리 ------------------------------

# 0 값을 평균으로 대체
df[columns_to_replace] = df[columns_to_replace].replace(0, np.nan)
for column in columns_to_replace:
    df[column].fillna(df[column].mean(), inplace=True)

# 이상치 처리할 열 리스트로 저장
colums_for_outliers = ['SkinThickness', 'Insulin']

# -------------------------------------------------

# ------- 이상치 처리 -------------------------------

# 이상치 처리 (상위 1% 값을 평균으로 대체)
for column in colums_for_outliers:
    # 상위 1% 값 계산
    threshold = df[column].quantile(0.99)
    
    # 상위 1% 값을 이상치를 제외한 나머지 데이터의 평균으로 대체
    df[column] = np.where(df[column] > threshold, df[column].mean(), df[column])

# -------------------------------------------------

# ------- 정규화 처리 -------------------------------

# MinMaxScaler 객체 생성
scaler = MinMaxScaler()

# Age 열을 MinMaxScaler로 0~1 범위로 정규화
df['Age'] = scaler.fit_transform(df[['Age']])

# -------------------------------------------------

# ------- EDA -------------------------------------

# 각 열의 결측치 개수 출력
print("\n------- 각 열의 결측치 개수 -------\n")
print(df.isnull().sum())

# Outcome 별 Glucose 평균 출력
print("\n------- Outcome 별 Glucose 평균 -------\n")
print(df.groupby('Outcome')['Glucose'].mean())

# 전처리 후 데이터 프레임 상위 5개 행 출력
print("\n------- 전처리 후 데이터 프레임 상위 5개 행 -------\ns")
print(df.head())

# -------------------------------------------------