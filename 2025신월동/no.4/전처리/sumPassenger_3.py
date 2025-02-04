import pandas as pd

# CSV 파일 로드
file_path = r'data-20250122T010720Z-001\data\bus_usage_with_stop_names_and_coords_cleaned.csv'
bus_usage = pd.read_csv(file_path)

# 승차정류장ID와 하차정류장ID가 같은 경우 승객수를 합산
grouped_bus_usage = bus_usage.groupby(['승차정류장ID', '하차정류장ID', '승차정류장명', '하차정류장명', '위도_x', '경도_x', '위도_y', '경도_y']).agg({'승객수': 'sum'}).reset_index()

# 새로운 CSV 파일로 저장
output_file_path = r'data-20250122T010720Z-001\data\bus_usage_grouped.csv'
grouped_bus_usage.to_csv(output_file_path, index=False)

print(f"승객수가 합산된 새로운 파일이 생성되었습니다: {output_file_path}")