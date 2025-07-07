"""
생성형 AI 활용을 위한 머신러닝 & 딥러닝 2번 문제 - 주택 가격 데이터를 활용한 회귀 모델 학습 및 예측

문제 상황
주택 가격 데이터를 기반으로 회귀 모델을 학습하여 주택 가격을 예측해야 합니다.

문제 정의 및 요구사항
- 데이터셋: train.csv (House Prices Dataset)
- 결측값 처리: 결측이 많은 열 삭제, LotFrontage는 평균으로 대체
- 범주형 데이터 인코딩: pd.get_dummies로 처리
- 불필요한 데이터 인코딩: Id
- 학습/테스트 데이터 분리: 8:2 비율
- 모델 학습: DecisionTreeRegressor
- 모델 평가: MAE, MSE, RMSE, R2 점수 출력
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기
df = pd.read_csv('train.csv')

# ------------------------------------
# 결측값 처리
# ------------------------------------
# Id,MSSubClass,MSZoning,LotFrontage,LotArea,Street,Alley,LotShape,LandContour,Utilities,LotConfig,LandSlope,Neighborhood,Condition1,Condition2,BldgType,HouseStyle,OverallQual,OverallCond,YearBuilt,YearRemodAdd,RoofStyle,RoofMatl,Exterior1st,Exterior2nd,MasVnrType,MasVnrArea,ExterQual,ExterCond,Foundation,BsmtQual,BsmtCond,BsmtExposure,BsmtFinType1,BsmtFinSF1,BsmtFinType2,BsmtFinSF2,BsmtUnfSF,TotalBsmtSF,Heating,HeatingQC,CentralAir,Electrical,1stFlrSF,2ndFlrSF,LowQualFinSF,GrLivArea,BsmtFullBath,BsmtHalfBath,FullBath,HalfBath,BedroomAbvGr,KitchenAbvGr,KitchenQual,TotRmsAbvGrd,Functional,Fireplaces,FireplaceQu,GarageType,GarageYrBlt,GarageFinish,GarageCars,GarageArea,GarageQual,GarageCond,PavedDrive,WoodDeckSF,OpenPorchSF,EnclosedPorch,3SsnPorch,ScreenPorch,PoolArea,PoolQC,Fence,MiscFeature,MiscVal,MoSold,YrSold,SaleType,SaleCondition,SalePrice

# 결측값이 많은 열 삭제
missing_percentage = df.isnull().mean() /len(df)
columns_to_drop = missing_percentage[missing_percentage > 0.5].index.tolist()
df.drop(columns=columns_to_drop, inplace=True)

# LotFrontage는 평균으로 대체
if 'LotFrontage' in df.columns:
    df['LotFrontage'].fillna(df['LotFrontage'].mean(), inplace=True)

# ------------------------------------
# 불필요한 데이터 인코딩
# ------------------------------------

# Id 열 삭제
df.drop(columns=['Id'], inplace=True)

# ------------------------------------
# 범주형 데이터 인코딩
# ------------------------------------

# pd.get_dummies로 범주형 데이터 인코딩
categorical_columns = df.select_dtypes(include=['object']).columns

# 원-핫 인코딩
df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

# ------------------------------------
# 학습/테스트 데이터 분리
# ------------------------------------

# 학습 및 테스트 데이터 분리
X = df.drop(columns=['SalePrice'])
y = df['SalePrice']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42
)

# ------------------------------------
# 모델 학습
# ------------------------------------

# DecisionTreeRegressor 모델 학습
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

# ------------------------------------
# 모델 예측 및 평가
# ------------------------------------

# 테스트 데이터 예측
y_pred = model.predict(X_test)

# 평가 지표 계산
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# 평가 지표 출력
print("\n------- 모델 평가 지표 -------\n")
print(f'Mean Absolute Error (MAE): {mae}')
print(f'Mean Squared Error (MSE): {mse}')
print(f'Root Mean Squared Error (RMSE): {rmse}')
print(f'R^2 Score: {r2}')
print("-----------------------------------\n")