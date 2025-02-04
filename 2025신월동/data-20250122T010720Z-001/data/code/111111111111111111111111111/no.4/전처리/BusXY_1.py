import pandas as pd
from shapely.geometry import Point
import geopandas as gpd

# 버스 정류장 정보 파일 로드
bus_stops_file_path = r'data-20250122T010720Z-001\data\code\bus.csv'
bus_stops = pd.read_csv(bus_stops_file_path, encoding='utf-8')

# X좌표 변환: DDDMMMMMM -> DDD + MM.MMMM/60
bus_stops['정류장X좌표'] = bus_stops['정류장X좌표'].astype(float)
bus_stops['정류장X좌표'] = bus_stops['정류장X좌표'] // 100 + (bus_stops['정류장X좌표'] % 100) / 60

# Y좌표 변환: DDDMMMMMM -> DDD + MM.MMMM/60
bus_stops['정류장Y좌표'] = bus_stops['정류장Y좌표'].astype(float)
bus_stops['정류장Y좌표'] = bus_stops['정류장Y좌표'] // 100 + (bus_stops['정류장Y좌표'] % 100) / 60

# GeoDataFrame 생성
gdf_busstops = gpd.GeoDataFrame(bus_stops, geometry=[Point(x, y) for x, y in zip(bus_stops['정류장X좌표'], bus_stops['정류장Y좌표'])])
gdf_busstops.crs = 'EPSG:4326'  # 최신 방식으로 좌표 참조 시스템 설정

# 위도와 경도 열 추가
gdf_busstops['위도'] = gdf_busstops.geometry.y
gdf_busstops['경도'] = gdf_busstops.geometry.x

# 정류장ID 기준으로 하나의 이름만 남기기
bus_stops_unique = gdf_busstops.groupby('정류장ID', as_index=False).first()[['정류장ID', '버스정류장명', '위도', '경도']]

# 새로운 CSV 파일로 저장
output_file_path = r'data-20250122T010720Z-001\data\code\bus_with_coords_unique.csv'
bus_stops_unique.to_csv(output_file_path, index=False)

print(f"위도와 경도가 추가된 새로운 파일이 생성되었습니다: {output_file_path}")