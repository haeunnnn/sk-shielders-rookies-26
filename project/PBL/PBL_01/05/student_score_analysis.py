# --------------------------------------------------------------------------------------------------------------------------------------------

# 생성형 AI 활용을 위한 파이썬 5번 문제 - 과목별 성적 분석을 통한 학생 성과 시각화

# 문제 상황
# 20명의 학생의 과목별 성적 데이터를 분석하여 통계적 인사이트를 시각적으로 제공하고자 합니다.

# 문제 정의 및 요구사항
# - StudentScoreAnalysis 클래스 정의
# - 이름: '학생1' ~ '학생20'
# - 과목: 수학, 영어, 과학 (각 50 ~ 100사이 난수)
# - 분석 요구사항
#   - 과목별 평균 점수 막대 그래프 시각화
#   - 평균 성적 상위 5명 막대 그래프 시각화

# --------------------------------------------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# StudentScoreAnalysis 클래스 정의
class StudentScoreAnalysis:
    def __init__(self):
        # 학생 수 20명 초기화
        self.num_students = 20
        
        # 이름: '학생1' ~ '학생20' 생성
        self.students = [f'학생{i+1}' for i in range(self.num_students)]
        
        # 과목: 수학, 영어, 과학
        self.subjects = ['수학', '영어', '과학']
        
        # 각 과목별 성적 (50 ~ 100 사이 난수) 생성
        data = {
            subject: np.random.randint(50, 101, size=self.num_students) 
            for subject in self.subjects
        }
        
        # 데이터프레임 생성 및 인덱스 설정
        self.df = pd.DataFrame(data, index=self.students)
        
        # 생성된 데이터 출력
        print(f"생성된 학생 수: {self.num_students} 명")
        print("------- 초기 5개 학생 데이터 -------")
        print(self.df.head())
        print("------------------------------------")


    # 과목별 평균 점수 막대 그래프 시각화
    def analyze_subject_averages(self):
        # 과목별 평균 점수 계산
        subject_averages = self.df.mean(axis=0)
        
        print("--------- 과목별 평균 점수 ---------")
        print(subject_averages)
        print("------------------------------------")
        
        # 시각화
        self._plot_bar_chart(
            data=subject_averages,
            title='과목별 평균 점수',
            xlabel='과목',
            ylabel='평균 점수',
            color='skyblue'
        )

    # 평균 성적 상위 5명 막대 그래프 시각화
    def analyze_top_students(self):
        # 상위 5명 초기화
        self.top_n = 5

        # 학생별 평균 성적 계산 (행별 평균)
        student_averages = self.df.mean(axis=1)
        
        # 평균 성적을 기준으로 내림차순 정렬하고 상위 N명 선택
        top_students = student_averages.sort_values(ascending=False).head(self.top_n)
        
        print(f"---------- 평균 성적 순위 ----------")
        print(top_students)
        print("--------------------------------------")
        
        # 시각화
        self._plot_bar_chart(
            data=top_students,
            title=f'평균 성적 상위 {self.top_n}명',
            xlabel='학생 이름',
            ylabel='평균 점수',
            color='lightcoral'
        )

    # 공통적으로 사용될 막대 그래프 시각화 로직
    def _plot_bar_chart(self, data, title, xlabel, ylabel, color):
        # 한글 폰트 설정
        plt.rcParams['font.family'] ='Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] =False

        # 그래프 크기 설정
        plt.figure(figsize=(10, 6))
        
        # 막대 그래프 그리기
        bars = plt.bar(data.index, data.values, color=color)

        # 각 막대 위에 수치 표시
        for bar in bars:
            yval = bar.get_height() # 막대의 높이 (값)
            plt.text(bar.get_x() + bar.get_width()/2, yval + (yval * 0.02),
                     f'{yval:.1f}', # 소수점 첫째 자리까지 표시 (정수라면 .0f)
                     ha='center',   # 수평 정렬: 중앙
                     va='bottom',   # 수직 정렬: 아래 (막대 위쪽에 위치)
                     fontsize=9,    # 폰트 크기
                     color='black') # 텍스트 색상
        
        # Y축의 최대값을 텍스트가 잘리지 않도록 조정 (최대값보다 10% 더 여유를 줌)
        plt.ylim(0, max(data.values) * 1.1)

        # 그래프 제목과 축 레이블 설정
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        # X축 레이블이 길 경우 회전하여 겹치지 않게 함
        plt.xticks(rotation=45, ha='right')
        # Y축에만 그리드 표시
        plt.grid(axis='y', linestyle='--', alpha=0.7) 
        # 그래프 요소들이 겹치지 않도록 자동 조정
        plt.tight_layout()
        
        # 그래프 출력
        plt.show()

# 실행 코드
if __name__ == "__main__":
    # StudentScoreAnalysis 객체 생성
    score_analyzer = StudentScoreAnalysis()

    # 과목별 평균 점수 분석 및 시각화 실행
    score_analyzer.analyze_subject_averages()

    # 평균 성적 상위 5명 분석 및 시각화 실행
    score_analyzer.analyze_top_students()
    