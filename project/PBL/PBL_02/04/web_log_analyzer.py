"""
생성형 AI 활용을 위한 머신러닝 & 딥러닝 4번 문제 - 웹 서버 로그 기반 악성 요청 탐지를 위한 분류 모델 구축

문제 상황
웹 서버 로그 데이터를 분석하여 악성 요청을 탐지하는 머신러닝 분류 모델을 구축해야합니다.

문제 정의 및 요구사항
- 데이터셋: web_server_logs_2.csv
- 전처리
    - timestamp → hour 추출
    - status_code → is_error, label 생성
- 모델
    - Logistic Regression
- 평가
    - Accuracy, Precision, Recall, F1-Score 출력
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# --------------------------------------
# 데이터 준비 및 전처리
# --------------------------------------

# 데이터 로드
df = pd.read_csv('web_server_logs_2.csv')

# timestamp 전처리
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour

# status_code 전처리
df['is_error'] = df['status_code'] >= 400
df['label'] = (df['status_code'] >= 400).astype(int)

# --------------------------------------
# 모델 구축 및 학습
# --------------------------------------

# 데이터 분할
X = df[['hour', 'is_error']]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2, random_state=42
)

# Logistic Regression 모델 학습
model = LogisticRegression()
model.fit(X_train, y_train)

# 모델 평가
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

"""
주요 평가 지표 해석

- 정확도(Accuracy): 1.00
    모델이 전체 예측 중 100%를 올바르게 분류했다. 300개의 테스트 데이터 중에서 단 하나의 오분류도 없이 모든 요청을 정확하게 정상 또는 악성으로 판단했다.

- 정밀도(Precision): 1.00
    모델이 '악성 요청'이라고 예측한 것들이 모두 실제 악성 요청이었고, '정상 요청'이라고 예측한 것들도 모두 실제 정상 요청이었다. 오탐(False Positive)이 전혀 없었다.

- 재현율(Recall): 1.00
    실제 악성 요청과 실제 정상 요청을 모두 100% 정확하게 찾아냈다. 즉, 모델이 놓친(False Negative) 악성 요청이나 정상 요청이 전혀 없었다.

- F1-Score: 1.00
    정밀도와 재현율의 균형을 나타내는 지표로, 두 지표가 모두 최고치를 기록했기 때문에 F1-Score 또한 1.00으로 나타났다. 이는 모델의 성능이 매우 견고하고 균형 잡혀 있다는 것을 의미한다.

결과에 대한 추가적인 고려사항
- 데이터의 단순성: 웹 서버 로그 데이터가 매우 규칙적이거나, status_code를 기반으로 label을 직접 만들었기 때문에 is_error 피처가 label과 거의 동일한 정보를 가지고 있을 수 있다. 
    즉, 모델이 복잡한 패턴을 학습하기보다는 is_error 여부를 그대로 label로 매핑한 것에 가깝다고 볼 수 있다. 실제 웹 서버 로그는 훨씬 더 다양하고 복잡한 패턴을 가지는 경우가 많다.
- 과적합(Overfitting) 가능성: 만약 실제 상황의 복잡한 데이터가 아닌, 학습 데이터에만 너무 맞춰져서 완벽한 성능을 내는 것이라면 과적합일 수 있다. 
    하지만 이 경우 is_error 피처가 label을 직접적으로 결정하기 때문에 과적합이라기보다는 데이터의 특성 때문에 나타난 결과일 가능성이 더 높다.
- 현실 세계 적용: 실제 운영 환경에서는 status_code 외에도 request_method, url, user_agent, response_time 등 훨씬 더 다양한 피처들을 활용하여 악성 요청을 탐지해야 한다. 
    status_code만으로 악성 요청을 판단하는 것은 너무 단순할 수 있으며, 정상적인 요청도 4xx 에러 코드를 반환할 수 있기 때문이다.
"""