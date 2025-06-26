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

# Annual Income, Spending Score 열만 사용
X = df[['Annual Income (k$)', 'Spending Score (1-100)']]

# 표준화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 학습/테스트 데이터 분리 (8:2)
X_train, X_test = train_test_split(X_scaled, test_size=0.2, random_state=42)

# ----------------------------------------
# 모델 학습
# ----------------------------------------

# 엘보우 기법으로 최적 k 결정
inertia = []
K_range = range(2, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_train)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(6, 4))
plt.plot(K_range, inertia, marker='o')
plt.title('Elbow Method')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia')
plt.show()

# 최적 k 선택 (예시: 5, 실제로는 위 그래프 보고 결정)
optimal_k = 5
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
kmeans.fit(X_train)

# 학습/테스트 데이터에 클러스터 할당
train_labels = kmeans.predict(X_train)
test_labels = kmeans.predict(X_test)

# ----------------------------------------
# 평가 및 시각화
# ----------------------------------------

# Silhouette Score 출력
train_silhouette = silhouette_score(X_train, train_labels)
test_silhouette = silhouette_score(X_test, test_labels)
print(f"Train Silhouette Score: {train_silhouette:.3f}")
print(f"Test Silhouette Score: {test_silhouette:.3f}")

# 학습 데이터 산점도
plt.figure(figsize=(6, 4))
sns.scatterplot(x=X_train[:, 0], y=X_train[:, 1], hue=train_labels, palette='Set2', legend='full')
plt.title('Train Data Clusters')
plt.xlabel('Annual Income (scaled)')
plt.ylabel('Spending Score (scaled)')
plt.show()

# 테스트 데이터 산점도
plt.figure(figsize=(6, 4))
sns.scatterplot(x=X_test[:, 0], y=X_test[:, 1], hue=test_labels, palette='Set2', legend='full')
plt.title('Test Data Clusters')
plt.xlabel('Annual Income (scaled)')
plt.ylabel('Spending Score (scaled)')
plt.show()

# 각 클러스터 특징 분석
X_train_df = pd.DataFrame(X_train, columns=['Annual Income (scaled)', 'Spending Score (scaled)'])
X_train_df['Cluster'] = train_labels
cluster_summary = X_train_df.groupby('Cluster').mean()
print("\n클러스터별 평균 (학습 데이터):")
print(cluster_summary)
