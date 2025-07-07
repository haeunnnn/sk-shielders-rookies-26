"""
생성형 AI 활용을 위한 머신러닝 & 딥러닝 5번 문제 - 고객 이탈 여부 예측을 위한 딥러닝 분류 모델 설계

문제 상황
고객 데이터를 기반으로 이탈 여부를 예측하는 딥러닝 분류 모델을 설계해야 합니다.

문제 정의 및 요구사항
- 데이터셋: customer_data_balanced.csv
- 전처리
    - ContractType → One-Hot 인코딩
    - StandardScaler로 정규화
- 모델
    - Dense 레이어 기반 MLP(Dropout 포함)
    - Sigmoid 출력, Binary Crossentropy 손실 함수
    - 클래스 불균형을 고려한 가중치 적용 (예: class_weights={0: 1.0, 1: 2.0})
- 평가
    - Accuracy, F1-Score, Confusion Martrix, classification_report 출력
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.utils.class_weight import compute_class_weight

# --------------------------------------
# 데이터 준비 및 전처리
# --------------------------------------

# 데이터 로드
df = pd.read_csv('customer_data_balanced.csv')

# ContractType One-Hot 인코딩
if 'ContractType' in df.columns:
    df = pd.get_dummies(df, columns=['ContractType'], drop_first=True)

# 타겟 변수와 피처 분리
X = df.drop('IsChurn', axis=1)
y = df['IsChurn']

# 데이터 정규화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# --------------------------------------
# 딥러닝 모델 설계 및 학습
# --------------------------------------

# 클래스 가중치 계산
classes = np.unique(y_train)
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=classes,
    y=y_train
)
class_weight_dict = dict(enumerate(class_weights))

# 입력 피처의 개수 정의
input_dim = X_train.shape[1]

# 모델 설계
model = Sequential([
    # 첫 번째 은닉 레이어
    Dense(64, activation='relu', input_shape=(input_dim,)),
    # 과적합 방지를 위한 Dropout
    Dropout(0.3),
    # 두 번째 은닉 레이어
    Dense(32, activation='relu'),
    # 과적합 방지를 위한 Dropout
    Dropout(0.2),
    # 출력 레이터
    Dense(1, activation='sigmoid')
])

# 모델 컴파일
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# 모델 구조 요약
model.summary()

# 모델 학습
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
history = model.fit(
    X_train, y_train,
    # 학습 데이터의 일부를 검증 세트로 사용
    validation_split=0.2,
    # 에포크 수(반복 학습 횟수)
    epochs=50,
    # 배치 크기(한 번에 처리할 데이터 수)
    batch_size=32,
    # 클래스 가중치 적용
    class_weight=class_weight_dict,
    callbacks=[early_stop],
    verbose=1
)

# --------------------------------------
# 모델 평가
# --------------------------------------

# 테스트 세트 예측
y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype(int)

# 평가 지표 출력
print(f"\nAccuracy: {accuracy_score(y_test, y_pred)}")
print(f"F1-Score: {f1_score(y_test, y_pred)}\n")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Confusion Matrix 시각화
plt.figure(figsize=(6, 4))
sns.heatmap(confusion_matrix(y_test, y_pred), 
            annot=True, fmt='d', cmap='Blues',
            xticklabels=['Predicted 0', 'Predicted 1'],
            yticklabels=['Actual 0', 'Actual 1'])
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

print("Classification Report:\n", classification_report(y_test, y_pred))

"""
모델 성능 평가 결과 분석

- 정확도(Accuracy): 0.68 (68%)
    모델은 전체 테스트 데이터 400개 중 214명의 정상 고객과 58명의 이탈 고객, 총 272명을 올바르게 분류했다. 
    이는 모델이 일정 수준의 예측 능력을 가지고 있음을 보여주지만, 비즈니스 관점에서 더 높은 정확도가 요구될 수 있다.

- 정상 고객(클래스 0) 예측 성능
    - 정밀도 (Precision): 0.70
        - 모델이 '정상 고객'이라고 예측한 경우, 70%가 실제로 정상 고객이었다. 
    - 재현율 (Recall): 0.86
        - 실제 정상 고객 248명 중 86%인 214명을 모델이 정상 고객으로 올바르게 찾아냈다.
    - F1-Score: 0.77
        - 정상 고객 분류 성능이 비교적 균형 잡혀있고 우수하다는 것을 보여준다.
    - 213명의 정상 고객을 정확히 맞췄고, 35명의 정상 고객을 이탈할 것이라고 잘못 예측했다. (False Positive)

- 이탈 고객(클래스 1) 예측 성능
    - 정밀도 (Precision): 0.63
        - 모델이 '이탈 고객'이라고 예측한 경우, 63%만이 실제로 이탈 고객이었다.
    - 재현율 (Recall): 0.39
        - 실제 이탈 고객 152명 중 38%인 58명만을 모델이 올바르게 탐지했다.
    - F1-Score: 0.48
        - 이탈 고객 예측에 대한 F1-Score는 정밀도에 비해 재현율이 낮아 전반적으로 아쉬운 성능을 보인다.
    - 59명의 이탈 고객만 정확히 맞췄고, 93명의 실제 이탈 고객을 놓쳤다. (False Negative)

결론 및 시사점
본 딥러닝 모델은 정상 고객을 분류하는 데는 상대적으로 높은 성능을 보였지만 이탈 고객을 실제로 탐지하는 능력(재현율)은 여전히 낮은 수준이다. 
특히 94명의 실제 이탈 고객을 놓쳤다는 점은 비즈니스 관점에서 개선해야할 부분이다.
이탈 고객을 선제적으로 파악하여 적절한 조치를 취해야 하는 목표를 고려할 때, 이탈 고객에 대한 재현율을 높이는 데 중점을 둔 추가적인 모델 최적화가 필요할 것 같다.
        
"""