# --------------------------------------------------------------------------------------------------------------------------------------------

# 생성형 AI 활용을 위한 파이썬 4번 문제 - 계열 매출 데이터를 활용한 월별 매출 분석

# 문제 상황
# 1년 간의 매출 데이터를 분석하여 월 별 매출 추이를 시각화해 비즈니스 인사이트를 도출하고자 합니다.

# 문제 정의 및 요구사항
# - SalesAnalysis 클래스 정의
# - 2024 1월 ~ 12월까지의 날짜 생성
# - 일 별 매출(1000 ~ 10000)을 난수로 생성하여 저장
# - 월 별 매출 총합 계산 후 시각화

# --------------------------------------------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# SalesAnalysis 클래스 정의
class SalesAnalysis:
    def __init__(self):
        # 2024년 1월 1일부터 12월 31일까지의 날짜 생성
        self.dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')

        # 일별 매출 데이터 생성 (1000 ~ 10000 범위의 난수)
        self.daily_sales = np.random.randint(1000, 10001, size=len(self.dates))

        # 데이터프레임 생성
        self.df = pd.DataFrame({'Date': self.dates, 'Sales': self.daily_sales})
        self.df.set_index('Date', inplace=True)
        
        # 데이터 출력
        print(f"기간: {self.df.index.min()} ~ {self.df.index.max()}")
        print(f"총 데이터 개수: {len(self.df)}")
        print("--------- 초기 5개 데이터 ---------")
        print(self.df.head())
        print("------------------------------------")


    # 월별 매출 총합 계산
    def analyze_and_visualize_monthly_sales(self):
        monthly_sales = self.df['Sales'].resample('MS').sum()
        
        # 월별 매출 총합 출력
        print("---------- 월별 매출 총합 ----------")
        print(monthly_sales)
        print("--------------------------------------")
        
        # 시각화
        self._plot_monthly_sales(monthly_sales)

    # 월별 매출 시각화
    def _plot_monthly_sales(self, monthly_sales):
        # 한글 폰트 설정
        plt.rcParams['font.family'] ='Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] =False

        plt.figure(figsize=(12, 6))
        
        # 선 그래프와 마커
        monthly_sales.plot(kind='line', marker='o')
        plt.title('2024년 월별 매출 추이')
        plt.xlabel('월')
        plt.ylabel('총 매출 (원)')
        plt.grid(True)
        
        # X축 레이블을 월 단위로 표시
        plt.xticks(monthly_sales.index, [f'{i.month}월' for i in monthly_sales.index])
        # 그래프 요소들이 겹치지 않도록 자동 조정
        plt.tight_layout()
        plt.show()

# 실행 코드
if __name__ == "__main__":
    # SalesAnalysis 객체 생성
    sales_analyzer = SalesAnalysis()

    # 월별 매출 분석 및 시각화 실행
    sales_analyzer.analyze_and_visualize_monthly_sales()