import pandas as pd
import plotly.express as px

# 데이터 로드
file1_path = r'data-20250122T010720Z-001\data\code\bus.csv'
file2_path = r'data-20250122T010720Z-001\data\sinwol_bus.csv'

# CSV 파일 읽기
routes_df = pd.read_csv(file1_path)  # 노선 정보
passenger_df = pd.read_csv(file2_path)  # 승객 수

# 승차정류장ID에 대한 노선ID와 버스노선명을 가져옵니다.
boarding_df = passenger_df.merge(routes_df[['정류장ID', '노선ID', '버스노선명']], 
                                   left_on='승차정류장ID', 
                                   right_on='정류장ID', 
                                   how='left')

# 하차정류장ID에 대한 노선ID와 버스노선명을 가져옵니다.
alighting_df = passenger_df.merge(routes_df[['정류장ID', '노선ID', '버스노선명']], 
                                    left_on='하차정류장ID', 
                                    right_on='정류장ID', 
                                    how='left', 
                                    suffixes=('_승차', '_하차'))

# 승차일과 하차일을 datetime 형식으로 변환
boarding_df['승차일'] = pd.to_datetime(boarding_df['승차일시']).dt.date
alighting_df['하차일'] = pd.to_datetime(alighting_df['하차일시']).dt.date

# 승차 인원 집계
daily_boarding = boarding_df.groupby(['노선ID', '버스노선명', '승차일']).agg(
    일일_승차인원=('승객수', 'sum')
).reset_index()

# 하차 인원 집계
daily_alighting = alighting_df.groupby(['노선ID', '버스노선명', '하차일']).agg(
    일일_하차인원=('승객수', 'sum')
).reset_index()

# 승차와 하차 데이터를 병합
merged_passengers = pd.merge(daily_boarding, daily_alighting, 
                              left_on=['노선ID', '버스노선명', '승차일'], 
                              right_on=['노선ID', '버스노선명', '하차일'], 
                              how='outer')

# 노선별 일평균 승하차 인원 계산
average_passengers = merged_passengers.groupby(['노선ID', '버스노선명']).agg(
    일평균_승차인원=('일일_승차인원', 'mean'),
    일평균_하차인원=('일일_하차인원', 'mean')
).reset_index()

# Plotly scatter plot 생성
fig = px.scatter(
    average_passengers,
    x='일평균_승차인원',
    y='일평균_하차인원',
    color='버스노선명',
    title='노선별 일평균 승하차 인원',
    labels={'일평균_승차인원': '일평균 승차 인원', '일평균_하차인원': '일평균 하차 인원'},
    hover_name='버스노선명'
)

# 특정 폴더 경로 지정
output_path = 'no.2/averageBoardingAlighting.html'

# 그래프를 지정한 경로에 HTML 파일로 저장
fig.write_html(output_path)