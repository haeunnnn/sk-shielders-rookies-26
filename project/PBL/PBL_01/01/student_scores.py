# --------------------------------------------------------------------------------------------------------------------------------------------

# 생성형 AI 활용을 위한 파이썬 1번 문제 - 학생 평균 성적 관리 프로그램

# 문제 상황
# 학생들의 성적 데이터를 분석해야 하는 상황에서 객체지향 프로그래밍(OOP)을 활용하여 데이터를 효율적으로 관리하고 분석하는 프로그램이 필요합니다.

# 문제 정의 및 요구사항
# - 파일: "scores_korean.txt" ("이름, 점수" 형식으로 저장된 학생 성적 데이터)
# - StudentScores 클래스 정의
# - 생성자(__init__) : 파일을 읽고 데이터를 딕셔너리에 저장
# - 평균 점수 계산 메서드(calculate_average())
# - 평균 이상 학생 리스트 반환 메서드 (get_above_average())
# - 평균 이하 학생 데이터를 별도 파일로 저장하는 메서드(save_below_average())
#   - 파일명 : "below_average_korean.txt"
# - 평균 점수와 평균 이상 학생 리스트 출력 메서드 (print_summary())

# --------------------------------------------------------------------------------------------------------------------------------------------

class StudentScores:
    # 학생 성적 데이터를 저장할 딕셔너리
    student_scores = {}

    # 생성자
    def __init__(self):
        # 파일을 읽고 데이터를 딕셔너리에 저장
        with open("scores_korean.txt", 'r', encoding='UTF-8') as f:
            for line in f:
                s_name, s_score = line.strip().split(',')
                self.student_scores[s_name] = int(s_score)

    # 평균 점수 계산 메서드
    def calculate_average(self):
        scores = list(self.student_scores.values())
        s_num = len(scores)
        
        return sum(scores) / s_num
    
    # 평균 이상 학생 리스트 반환 메서드
    def get_above_average(self):
        avg_score = self.calculate_average()
        above_avg_students = list(filter(lambda s: self.student_scores[s] >= avg_score, self.student_scores))
        
        return above_avg_students

    # 평균 이하 학생 데이터를 별도 파일로 저장하는 메서드
    def save_below_average(self):
        avg_score = self.calculate_average()
        below_avg_students = list(filter(lambda s: self.student_scores[s] <= avg_score, self.student_scores))

        with open("below_average_korean.txt", "w", encoding='UTF-8') as f:
            f.write("--- 평균 이하 학생들 정보 ---\n")
            for s in below_avg_students:
                s_score = self.student_scores[s]

                f.write(f"이름: {s}, 점수: {s_score}\n")

    # 평균 점수와 평균 이상 학생 리스트 출력 메서드
    def print_summary(self):
        print("------ 평균 점수와 평균 이상 학생 리스트 ------")
        print(f"평균 점수: {self.calculate_average()} 점")
        print(f"평균 이상 학생 리스트: {self.get_above_average()}")
        print("------------------------------------------------")

# 테스트
st_1 = StudentScores()

st_1.calculate_average()
st_1.get_above_average()
st_1.save_below_average()
st_1.print_summary()