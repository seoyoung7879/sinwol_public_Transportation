import pandas as pd

# 버스 이용 정보 파일 로드
bus_usage_file_path = r'data-20250122T010720Z-001\data\sinwol_bus.csv'
bus_usage = pd.read_csv(bus_usage_file_path)

# 버스 정류장 정보 파일 로드
bus_stops_file_path = r'data-20250122T010720Z-001\data\code\bus_with_coords_unique.csv'
bus_stops = pd.read_csv(bus_stops_file_path, encoding='utf-8')

# 지하철 정보 파일 로드
subway_stops_file_path = r'data-20250122T010720Z-001\data\code\subway_with_coords_unique.csv'
subway_stops = pd.read_csv(subway_stops_file_path, encoding='utf-8')

# 버스 정류장 정보와 조인
bus_usage = bus_usage.merge(bus_stops[['정류장ID', '버스정류장명', '위도', '경도']], left_on='승차정류장ID', right_on='정류장ID', how='left')
bus_usage.rename(columns={'버스정류장명': '승차정류장명', '위도': '위도_x', '경도': '경도_x'}, inplace=True)
bus_usage.drop(columns=['정류장ID'], inplace=True)

# 지하철 정류장 정보와 조인 (버스 정류장 정보가 없는 경우)
bus_usage = bus_usage.merge(subway_stops[['역ID', '역명', '위도', '경도']].rename(columns={'역ID': '승차정류장ID', '역명': '승차정류장명', '위도': '위도_subway', '경도': '경도_subway'}), on='승차정류장ID', how='left', suffixes=('', '_subway'))
bus_usage['승차정류장명'] = bus_usage['승차정류장명'].combine_first(bus_usage['승차정류장명_subway'])
bus_usage['위도_x'] = bus_usage['위도_x'].combine_first(bus_usage['위도_subway'])
bus_usage['경도_x'] = bus_usage['경도_x'].combine_first(bus_usage['경도_subway'])
bus_usage.drop(columns=['승차정류장명_subway', '위도_subway', '경도_subway'], inplace=True)

# 하차 정류장 정보와 조인
bus_usage = bus_usage.merge(bus_stops[['정류장ID', '버스정류장명', '위도', '경도']], left_on='하차정류장ID', right_on='정류장ID', how='left')
bus_usage.rename(columns={'버스정류장명': '하차정류장명', '위도': '위도_y', '경도': '경도_y'}, inplace=True)
bus_usage.drop(columns=['정류장ID'], inplace=True)

# 지하철 정류장 정보와 조인 (버스 정류장 정보가 없는 경우)
bus_usage = bus_usage.merge(subway_stops[['역ID', '역명', '위도', '경도']].rename(columns={'역ID': '하차정류장ID', '역명': '하차정류장명', '위도': '위도_subway', '경도': '경도_subway'}), on='하차정류장ID', how='left', suffixes=('', '_subway'))
bus_usage['하차정류장명'] = bus_usage['하차정류장명'].combine_first(bus_usage['하차정류장명_subway'])
bus_usage['위도_y'] = bus_usage['위도_y'].combine_first(bus_usage['위도_subway'])
bus_usage['경도_y'] = bus_usage['경도_y'].combine_first(bus_usage['경도_subway'])
bus_usage.drop(columns=['하차정류장명_subway', '위도_subway', '경도_subway'], inplace=True)

# 필요한 열만 남기기
bus_usage = bus_usage[['교통수단코드', '승차일시', '승차정류장ID', '하차일시', '하차정류장ID', '승객수', '승차정류장명', '위도_x', '경도_x', '하차정류장명', '위도_y', '경도_y']]

# 결측값이 있는 행 제거
bus_usage.dropna(subset=['승차정류장명', '위도_x', '경도_x'], inplace=True)

# 새로운 CSV 파일로 저장
output_file_path = r'C:\Users\USER\Desktop\2025신월동\data-20250122T010720Z-001\data\bus_usage_with_stop_names_and_coords_cleaned.csv'
bus_usage.to_csv(output_file_path, index=False)

print(f"정류장 이름과 위도/경도가 추가된 새로운 파일이 생성되었습니다: {output_file_path}")

# CSV 파일 로드
file_path = output_file_path
bus_usage = pd.read_csv(file_path)

# 결측값 확인
missing_values = bus_usage.isnull().sum()

# 결측값이 있는 열만 출력
missing_values = missing_values[missing_values > 0]

print("결측값이 있는 열과 그 개수:")
print(missing_values)