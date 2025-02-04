import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 경우 맑은 고딕 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 데이터 로드
file_path = r'data-20250122T010720Z-001\data\bus_usage_grouped.csv'
df = pd.read_csv(file_path)

# 승객수 요약 통계 계산
summary_stats = df['승객수'].describe()

# 요약 통계 출력
print("승객수 요약 통계:")
print(summary_stats)

# 승객수 상위 25% 데이터 필터링
upper_25_percent_threshold = df['승객수'].quantile(0.75)
upper_25_percent_data = df[df['승객수'] >= upper_25_percent_threshold]

# 상위 25% 승객수 요약 통계 계산
upper_25_summary_stats = upper_25_percent_data['승객수'].describe()

# 상위 25% 요약 통계 출력
print("\n상위 25% 승객수 요약 통계:")
print(upper_25_summary_stats)

# 상위 25% 승객수 히스토그램 그리기
plt.figure(figsize=(10, 6))
plt.hist(upper_25_percent_data['승객수'], bins=30, edgecolor='black', alpha=0.7)
plt.title('상위 25% 승객수 히스토그램')
plt.xlabel('승객수')
plt.ylabel('빈도수')
plt.grid(True)
plt.show()