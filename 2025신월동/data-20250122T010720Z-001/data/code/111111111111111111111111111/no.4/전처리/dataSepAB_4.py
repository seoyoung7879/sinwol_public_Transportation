import pandas as pd

# 데이터 로드
df = pd.read_csv(r'data-20250122T010720Z-001\data\bus_usage_grouped.csv')

# 새로운 파일 2 로드 (신월동의 정류장 ID를 확인)
sinwol_stops = pd.read_csv(r'data-20250122T010720Z-001\data\sinwol_busstops.csv')  # 파일 2 경로

# 신월동 정류장 ID 목록 추출
sinwol_stops_ids = sinwol_stops['정류장ID'].tolist()

# 1. 신월동에서 출발한 데이터 (출발 정류장이 신월동 정류장에 해당하는 경우)
sinwol_departures = df[df['승차정류장ID'].isin(sinwol_stops_ids)]

# 2. 신월동으로 도착한 데이터 (도착 정류장이 신월동 정류장에 해당하는 경우)
sinwol_arrivals = df[df['하차정류장ID'].isin(sinwol_stops_ids)]

# 신월동에서 출발한 데이터의 승객수를 도착지만 같으면 합산
sinwol_departures_grouped = sinwol_departures.groupby(['하차정류장ID', '하차정류장명', '위도_y', '경도_y']).agg({'승객수': 'sum'}).reset_index()

# 신월동으로 도착한 데이터의 승객수를 출발지만 같으면 합산
sinwol_arrivals_grouped = sinwol_arrivals.groupby(['승차정류장ID', '승차정류장명', '위도_x', '경도_x']).agg({'승객수': 'sum'}).reset_index()

# 신월동에서 출발한 데이터 저장
sinwol_departures_file_path = r'data-20250122T010720Z-001\data\sinwol_departures_grouped.csv'
sinwol_departures_grouped.to_csv(sinwol_departures_file_path, index=False)

# 신월동으로 도착한 데이터 저장
sinwol_arrivals_file_path = r'data-20250122T010720Z-001\data\sinwol_arrivals_grouped.csv'
sinwol_arrivals_grouped.to_csv(sinwol_arrivals_file_path, index=False)

print(f"신월동에서 출발한 데이터가 저장되었습니다: {sinwol_departures_file_path}")
print(f"신월동으로 도착한 데이터가 저장되었습니다: {sinwol_arrivals_file_path}")