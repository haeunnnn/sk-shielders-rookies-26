# --------------------------------------------------------------------------------------------------------------------------------------------

# 생성형 AI 활용을 위한 파이썬 6번 문제 - 고객 구매 데이터를 활용한 매출 및 기여도 분석

# 문제 상황
# 고객의 구매 데이터를 기반으로 마케팅 전략 수립을 위한 월별 매출 고객별 누적 기여도 분석이 필요합니다.

# 문제 정의 및 요구사항
# - CustomerSalesAnalysis 클래스 정의
# - 데이터 항목: 고객명, 구매일자, 상품명, 수량, 단가
# - 분석 및 시각화
#   - 월별 매출 총합 막대 그래프
#   - 고객별 누적 매출 파이 차트

# --------------------------------------------------------------------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from datetime import datetime, timedelta

# CustomerSalesAnalysis 클래스 정의
class CustomerSalesAnalysis:
    def __init__(self, data):
        # 고객명, 구매일자, 상품명, 수량, 단가 정보를 포함하는 리스트
        self.df = pd.DataFrame(data, columns=['고객명', '구매일자', '상품명', '수량', '단가'])
        self._preprocess_data()

    # 데이터 전처리
    def _preprocess_data(self):
        # '구매일자'를 datetime 형식으로 변환
        self.df['구매일자'] = pd.to_datetime(self.df['구매일자'])
        # '총매출' (수량 * 단가) 열 생성
        self.df['총매출'] = self.df['수량'] * self.df['단가']
    
    # 월별 매출 총합을 분석하고 막대 그래프로 시각화
    def analyze_monthly_sales(self):
        # 한글 폰트 설정 (Windows 기준)
        plt.rcParams['font.family'] = 'Malgun Gothic'
        # 마이너스 기호 깨짐 방지
        plt.rcParams['axes.unicode_minus'] = False

        # 월별 매출 집계
        self.df['월'] = self.df['구매일자'].dt.to_period('M')
        monthly_sales = self.df.groupby('월')['총매출'].sum().sort_index()

        print("--------- 월별 매출 총합 ---------")
        print(monthly_sales)
        print("-" * 36)

        # 월별 매출 막대 그래프 시각화

        # 그래프 크기 설정
        plt.figure(figsize=(12, 6))

        bars = plt.bar(monthly_sales.index.astype(str), monthly_sales.values, color='skyblue')
        plt.title('월별 매출 총합')
        plt.xlabel('월')
        plt.ylabel('총매출')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # 각 막대 위에 매출 값 표시
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, f'{yval:,.0f}', ha='center', va='bottom') # 천 단위 쉼표 추가

        # y축 포맷터 설정 (천 단위 쉼표)
        formatter = mticker.FormatStrFormatter('%1.0f')
        plt.gca().yaxis.set_major_formatter(formatter)

        plt.show()

    # 고객별 누적 매출을 분석하고 파이 차트로 시각화
    def analyze_customer_contribution(self):
        # 고객별 총매출 집계
        customer_sales = self.df.groupby('고객명')['총매출'].sum().sort_values(ascending=False)

        print("--------- 고객별 누적 매출 ---------")
        print(customer_sales)
        print("-" * 36)

        # 그래프 크기 설정
        plt.figure(figsize=(10, 10))

        # 고객별 누적 매출 파이 차트 시각화
        wedges, texts, autotexts = plt.pie(
            customer_sales,
            labels=customer_sales.index,
            autopct=lambda p: '{:.1f}% ({:,.0f})'.format(p, p * sum(customer_sales) / 100), # %와 값 함께 표시, 천 단위 쉼표
            startangle=90,
            pctdistance=0.85    # 텍스트와 파이 차트 중심 사이의 거리
        )
        plt.title('고객별 누적 매출 기여도')
        # 파이 차트를 원형으로 유지
        plt.axis('equal')
        plt.show()


"""
랜덤으로 고객 구매 데이터를 생성

Args:
    num_customers (int): 생성할 고객의 수
    num_products (int): 생성할 상품의 수
    num_transactions (int): 생성할 거래 기록의 수
    start_date (str): 데이터 생성 시작일 (YYYY-MM-DD)
    end_date (str): 데이터 생성 종료일 (YYYY-MM-DD)
"""
def generate_random_sales_data(num_customers=10, num_products=20, num_transactions=200, start_date='2023-01-01', end_date='2023-12-31'):
    # 고객1, 고객2, 고객3, ...
    customers = [f'고객{i+1}' for i in range(num_customers)]
    # A, B, C, ...
    products = [f'상품{chr(65+i)}' for i in range(min(num_products, 26))] 
    # 26개를 초과하면 숫자도 사용하도록 함
    if num_products > 26:
        products.extend([f'상품{i}' for i in range(27, num_products + 1)])

    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    time_delta = end_datetime - start_datetime

    # 고객 데이터를 랜덤으로 생성하여 리스트에 저장
    data = []
    for _ in range(num_transactions):
        customer = np.random.choice(customers)
        product = np.random.choice(products)
        
        # 구매일자 랜덤 생성
        random_days = np.random.randint(0, time_delta.days)
        purchase_date = (start_datetime + timedelta(days=random_days)).strftime('%Y-%m-%d')

        # 수량 1개에서 10개 사이
        quantity = np.random.randint(1, 10)
        # 단가 1만원에서 10만원 사이
        unit_price = np.random.randint(10000, 100000)

        data.append([customer, purchase_date, product, quantity, unit_price])
    return data

# 실행 코드
if __name__ == "__main__":
    # 랜덤 데이터 생성 (예: 고객 15명, 상품 30개, 거래 300건, 2023년 전체 데이터)
    random_sales_data = generate_random_sales_data(
        num_customers=15,
        num_products=30,
        num_transactions=300,
        start_date='2023-01-01',
        end_date='2023-12-31'
    )

    # CustomerSalesAnalysis 인스턴스 생성 및 분석 실행
    analyzer = CustomerSalesAnalysis(random_sales_data)

    # 월별 매출 총합을 분석하고 막대 그래프로 시각화
    analyzer.analyze_monthly_sales()

    # 고객별 누적 매출을 분석하고 파이 차트로 시각화
    analyzer.analyze_customer_contribution()