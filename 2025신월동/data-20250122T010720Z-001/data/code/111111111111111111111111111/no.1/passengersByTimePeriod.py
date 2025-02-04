import pandas as pd
import plotly.express as px

# CSV 파일 읽기
bus_data = pd.read_csv('data-20250122T010720Z-001/data/sinwol_bus.csv')

# 승차일시와 하차일시를 datetime 형식으로 변환
bus_data['승차일시'] = pd.to_datetime(bus_data['승차일시'], format='%Y%m%d%H%M%S')
bus_data['하차일시'] = pd.to_datetime(bus_data['하차일시'], format='%Y%m%d%H%M%S')

# 시간대 추가 (00시도 00:00으로 출력되도록 포맷 설정)
bus_data['승차시간대'] = bus_data['승차일시'].dt.floor('H').dt.strftime('%H:%M')  # 시간 단위로 내림 후 포맷
bus_data['하차시간대'] = bus_data['하차일시'].dt.floor('H').dt.strftime('%H:%M')  # 시간 단위로 내림 후 포맷

# 승차와 하차 인원수 집계
boarding_counts = bus_data.groupby('승차시간대')['승객수'].sum().reset_index(name='승차인원수')
alighting_counts = bus_data.groupby('하차시간대')['승객수'].sum().reset_index(name='하차인원수')

# 시간대별 승하차 인원 통합
combined_counts = pd.merge(boarding_counts, alighting_counts, left_on='승차시간대', right_on='하차시간대', how='outer')

# 시각화
fig = px.bar(combined_counts, 
             x='승차시간대', 
             y=['승차인원수', '하차인원수'], 
             title='시간대별 승하차 인원',
             labels={'value': '인원수', 'variable': '승하차'},
             barmode='stack',  # 스택형 막대그래프
             color_discrete_sequence=['blue', 'red'])  # 승차는 파랑, 하차는 빨강

# x축 레이블 변경
fig.update_layout(xaxis_title='시간대')  # x축 이름을 '시간대'로 변경

# 특정 폴더 경로 지정
output_path = 'no.1/PassengerByTImePeriod.html'

# 그래프를 지정한 경로에 HTML 파일로 저장
fig.write_html(output_path)