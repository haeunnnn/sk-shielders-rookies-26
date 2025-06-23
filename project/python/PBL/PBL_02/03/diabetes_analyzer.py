"""
생성형 AI 활용을 위한 머신러닝 & 딥러닝 3번 문제 - 고객 데이터를 활용한 K-Means 클러스터링 분석

문제 상황
고객 데이터를 K-Means 클러스터링을 통해 세분화하고, 그 결과를 평가해야 합니다.

문제 정의 및 요구사항
- 데이터셋: Mall_Customers.csv
- 전처리
    - Annual Income, Spending Score 열 사용
    - StandardScaler로 표준화
    - 학습/테스트 데이터 분리 (8:2)
- 모델 학습
    - 엘보우 기법으로 최적 k 결정
    - Kmeans로 학습 후 테스트 데이터에 적용
- 평가 및 시각화
    - Silhouette Score 출력
    - 학습/테스트 결과 산점도 시각화
    - 각 클러스터 특징 분석
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기
df = pd.read_csv('Mall_customers.csv')

# ----------------------------------------
# 전처리
# ----------------------------------------

# ----------------------------------------
# 모델 학습
# ----------------------------------------

# ----------------------------------------
# 평가 및 시각화
# ----------------------------------------

