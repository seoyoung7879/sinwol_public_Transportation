import pandas as pd
import plotly.express as px

# CSV 파일 읽기
bus_data = pd.read_csv('data-20250122T010720Z-001/data/sinwol_bus.csv')

# 승차일시를 datetime 형식으로 변환
bus_data['승차일시'] = pd.to_datetime(bus_data['승차일시'], format='%Y%m%d%H%M%S')

# 요일 및 시간대 추가
bus_data['승차요일'] = bus_data['승차일시'].dt.day_name()
bus_data['승차시간대'] = bus_data['승차일시'].dt.floor('H').dt.strftime('%H:%M')  # 시간 단위로 내림 후 포맷

# 승차 인원수 집계
boarding_counts = bus_data.groupby(['승차요일', '승차시간대'])['승객수'].sum().reset_index(name='승차인원수')

# 요일 순서 설정 (월화수목금토일)
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
boarding_counts['승차요일'] = pd.Categorical(boarding_counts['승차요일'], categories=days_order, ordered=True)

# 요일 순서가 적용된 데이터프레임 정렬
boarding_counts = boarding_counts.sort_values(['승차요일', '승차시간대'])

# 시각화
fig = px.line(boarding_counts, 
              x='승차시간대', 
              y='승차인원수', 
              color='승차요일', 
              title='요일 및 시간대별 승차 인원',
              labels={'승차시간대': '시간대', '승차인원수': '인원수'},
              markers=True)  # 마커 추가

# 그래프 출력
fig.update_layout(legend=dict(traceorder="normal"))  # 범례 순서 월화수목금토일 적용
# 특정 폴더 경로 지정
output_path = 'no.1/PassengerByWeekdayAndTime_boarding.html'

# 그래프를 지정한 경로에 HTML 파일로 저장
fig.write_html(output_path)


