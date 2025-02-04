import pandas as pd
import plotly.express as px

# CSV 파일 읽기
bus_data = pd.read_csv('data-20250122T010720Z-001/data/sinwol_bus.csv')

# 하차일시를 datetime 형식으로 변환
bus_data['하차일시'] = pd.to_datetime(bus_data['하차일시'], format='%Y%m%d%H%M%S')

# 요일 및 시간대 추가
bus_data['하차요일'] = bus_data['하차일시'].dt.day_name()
bus_data['하차시간대'] = bus_data['하차일시'].dt.floor('H').dt.strftime('%H:%M')  # 시간 단위로 내림 후 포맷

# 하차 인원수 집계
alighting_counts = bus_data.groupby(['하차요일', '하차시간대'])['승객수'].sum().reset_index(name='하차인원수')

# 요일 순서 설정 (월화수목금토일)
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
alighting_counts['하차요일'] = pd.Categorical(alighting_counts['하차요일'], categories=days_order, ordered=True)

# 시각화
fig = px.line(
    alighting_counts.sort_values(by=['하차요일', '하차시간대']),  # 요일 및 시간대 순서 정렬
    x='하차시간대',
    y='하차인원수',
    color='하차요일',
    title='요일 및 시간대별 하차 인원',
    labels={'하차시간대': '시간대', '하차인원수': '인원수'},
    markers=True  # 마커 추가
)

# 범례 순서 설정
fig.for_each_trace(lambda t: t.update(name=t.name.split(' ')[0]))  # 요일 이름에서 공백 제거

# 특정 폴더 경로 지정
output_path = 'no.1/PassengerByWeekdayAndTime_alighting.html'

# 그래프를 지정한 경로에 HTML 파일로 저장
fig.write_html(output_path)


