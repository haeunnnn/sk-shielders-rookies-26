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
df = pd.read_csv('Mall_Customers.csv')

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
print(f"{cluster_summary}\n")

"""
K-Means 클러스터링 기반 고객 세분화

1. 일반 고객층 (Cluster 0)
- 특징: 연간 소득과 소비 점수 모두 평균과 유사한 고객 그룹. 데이터 상으로는 스케일링된 값들이 0에 가깝게 분포.
- 인사이트: 이들은 쇼핑몰의 주류 고객층으로, 안정적인 매출을 발생시키는 중요한 기반이 된다. 특별히 튀는 소비 패턴은 없지만, 꾸준히 방문하고 구매하는 경향이 있을 것이다.
- 마케팅 전략
    - 유지 및 육성: 이탈을 방지하고 구매 빈도나 객단가를 소폭 늘릴 수 있는 일반적인 프로모션, 시즌 할인, 신상품 안내 등을 꾸준히 제공
    - 잠재력 발굴: 구매 이력 데이터를 활용하여 관심사를 파악하고, 개인화된 상품 추천을 통해 특정 카테고리에서의 소비를 유도할 수 있다.

2. 절약형 고객층 (Cluster 1)
- 특징: 연간 소득과 소비 점수 모두 평균보다 현저히 낮은 고객 그룹
- 인사이트: 소득이 낮고 소비 지출도 적어 쇼핑몰에서의 적극적인 구매 활동을 기대하기는 어려울 것. 가격에 매우 민감하며, 필수품 위주로 구매할 가능성이 높다.
- 마케팅 전략
    - 가성비 강조: 초특가 할인, 묶음 할인, 저가형 상품군을 중심으로 홍보하여 가격 경쟁력을 어필.
    - 충성도 확보: 포인트 적립률을 높이거나, 할인 쿠폰을 주기적으로 제공하여 재방문을 유도하고 장기적인 관계를 구축.

3. 알뜰 쇼핑형 고객층 (Cluster 2)
- 특징: 연간 소득은 평균보다 현저히 낮지만, 소비 점수는 평균보다 현저히 높은 고객 그룹
- 인사이트: 소득 수준은 낮지만 쇼핑을 즐기거나 특정 품목에 대한 지출이 큰 '가심비'를 추구하는 고객층으로 보임. 제한된 예산 안에서 최대의 만족을 얻으려 한다.
- 마케팅 전략
    - 가심비/할인 기회 제공: 핫딜, 타임 세일, 멤버십 전용 할인 등 구매 시 '이득을 본다'는 느낌을 줄 수 있는 프로모션.
    - 선택과 집중: 이들이 주로 구매하는 품목이나 선호하는 브랜드에 대한 맞춤형 추천을 강화.

4. VIP 고객층 (Cluster 3)
- 특징: 연간 소득과 소비 점수 모두 평균보다 현저히 높은 고객 그룹
- 인사이트: 쇼핑몰의 핵심 매출을 견인하는 가장 중요한 고객층. 구매력이 높고 소비 지출도 활발하여 프리미엄 서비스와 고가 상품에 반응할 가능성이 높다.
- 마케팅 전략:
    - 프리미엄 대우: VIP 전용 이벤트, 독점 할인, 신상품 선공개, 맞춤형 컨시어지 서비스 등을 통해 특별함을 느끼게 해야 한다.
    - 로열티 강화: 높은 수준의 포인트 적립, 무료 배송/반품 혜택 등을 제공하여 장기적인 충성도를 확보하고 이탈을 방지한다.

5. 잠재 VIP 고객층 (Cluster 4)
- 특징: 연간 소득은 평균보다 현저히 높지만, 소비 점수는 평균보다 현저히 낮은 고객 그룹
- 인사이트: 높은 구매력을 가지고 있음에도 현재 쇼핑몰에서의 지출이 적은 고객층. 다른 곳에서 소비하거나 아직 쇼핑몰의 매력을 충분히 느끼지 못했을 수 있다.
- 마케팅 전략:
    - 구매 유도: 이들의 소득 수준에 맞는 고품질/고가 상품군을 제안하고, 흥미를 유발할 수 있는 테마 기획전 등을 통해 방문과 구매를 유도한다.
    - 혜택 어필: VIP 서비스나 프리미엄 멤버십의 장점을 명확히 안내하여, 잠재된 소비를 활성화할 수 있는 동기를 부여한다.

"""