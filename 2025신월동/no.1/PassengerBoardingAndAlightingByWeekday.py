import pandas as pd
import plotly.express as px

# CSV 파일 읽기
bus_data = pd.read_csv('data-20250122T010720Z-001/data/sinwol_bus.csv')

# 승차일시와 하차일시를 datetime 형식으로 변환
bus_data['승차일시'] = pd.to_datetime(bus_data['승차일시'], format='%Y%m%d%H%M%S')
bus_data['하차일시'] = pd.to_datetime(bus_data['하차일시'], format='%Y%m%d%H%M%S')

# 요일 정보 추출 (0=월요일, 6=일요일)
bus_data['승차요일'] = bus_data['승차일시'].dt.day_name()  # 요일명 추출
bus_data['하차요일'] = bus_data['하차일시'].dt.day_name()  # 요일명 추출

# 요일 순서를 설정
ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
bus_data['승차요일'] = pd.Categorical(bus_data['승차요일'], categories=ordered_days, ordered=True)
bus_data['하차요일'] = pd.Categorical(bus_data['하차요일'], categories=ordered_days, ordered=True)

# 요일별 승차와 하차 인원수 집계 (observed=False 추가)
boarding_counts = bus_data.groupby('승차요일', observed=False)['승객수'].sum().reset_index(name='승차인원수')
alighting_counts = bus_data.groupby('하차요일', observed=False)['승객수'].sum().reset_index(name='하차인원수')

# 요일별 승하차 인원 통합
combined_counts = pd.merge(boarding_counts, alighting_counts, left_on='승차요일', right_on='하차요일', how='outer')

# 시각화 (grouped bar로 승차와 하차 인원 나란히 비교)
fig = px.bar(combined_counts, 
             x='승차요일', 
             y=['승차인원수', '하차인원수'], 
             title='요일별 승하차 인원',
             labels={'value': '인원수', 'variable': '승하차'},
             barmode='group',  # grouped bar 형식
             color_discrete_sequence=['blue', 'red'])  # 승차는 파랑, 하차는 빨강

# 특정 폴더 경로 지정
output_path = 'no.1/PassengerBoardingAndAlightingByWeekday.html'

# 그래프를 지정한 경로에 HTML 파일로 저장
fig.write_html(output_path)

