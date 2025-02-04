import pandas as pd
import plotly.express as px

# 버스 데이터 읽기
bus_data = pd.read_csv('data-20250122T010720Z-001/data/sinwol_bus.csv')

# 정류장 데이터 읽기 (정류장 ID와 이름이 포함된 파일)
bus_stops_data = pd.read_csv('data-20250122T010720Z-001/data/sinwol_busstops.csv')

# 하차일시를 datetime 형식으로 변환
bus_data['하차일시'] = pd.to_datetime(bus_data['하차일시'], format='%Y%m%d%H%M%S')

# 정류장별 하차 인원수 집계
alighting_counts = bus_data.groupby('하차정류장ID')['승객수'].sum().reset_index(name='하차인원수')

# 정류장 ID와 이름 매핑
# 정류장 ID를 인덱스로 설정하여 매핑
bus_stops_mapping = bus_stops_data.set_index('정류장ID')['버스정류장명'].to_dict()

# 정류장 ID에 이름 추가
alighting_counts['버스정류장명'] = alighting_counts['하차정류장ID'].map(bus_stops_mapping)

# 정류장명에 대해 총 하차 인원수 집계
total_alighting_counts = alighting_counts.groupby('버스정류장명')['하차인원수'].sum().reset_index()

# 하차 인원수에 따라 내림차순 정렬 (정류장명 기준)
total_alighting_counts = total_alighting_counts.sort_values(by='하차인원수', ascending=False)

# 시각화
fig = px.bar(total_alighting_counts, 
             x='버스정류장명', 
             y='하차인원수', 
             title='정류장별 하차 인원',
             labels={'버스정류장명': '정류장', '하차인원수': '하차 인원'},
             color='하차인원수',  # 색상으로 하차 인원수 표현
             text='하차인원수')  # 막대 위에 인원수 표시

# y축 범위 조정 (20,000까지 표시)
fig.update_yaxes(range=[0, 15000])  # y축 범위를 0에서 20,000으로 설정

# 특정 폴더 경로 지정
output_path = 'no.3/BusStopAlighting.html'

# 그래프를 지정한 경로에 HTML 파일로 저장
fig.write_html(output_path)
