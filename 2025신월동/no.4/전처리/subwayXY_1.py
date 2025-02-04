import pandas as pd

# 지하철 정보 파일 로드
subway_stops_file_path = r'data-20250122T010720Z-001\data\code\subway.csv'
subway_stops = pd.read_csv(subway_stops_file_path, encoding='utf-8')

# 서울시 역사마스터 정보 파일 로드 (인코딩 문제 해결)
subway_master_file_path = r'data-20250122T010720Z-001\data\code\서울시 역사마스터 정보.csv'
subway_master = pd.read_csv(subway_master_file_path, encoding='cp949')

# 열 이름 변경 (한글 깨짐 해결)
subway_master.columns = ['역ID', '역명', '호선명', '위도', '경도']

# 지하철 정보와 서울시 역사마스터 정보를 역ID를 기준으로 병합
subway_stops = subway_stops.merge(subway_master[['역ID', '위도', '경도']], on='역ID', how='left')

# 역ID 기준으로 하나의 이름만 남기기
subway_stops_unique = subway_stops.groupby('역ID', as_index=False).first()[['역ID', '역명', '위도', '경도']]

# 새로운 CSV 파일로 저장
output_file_path = r'data-20250122T010720Z-001\data\code\subway_with_coords_unique.csv'
subway_stops_unique.to_csv(output_file_path, index=False)

print(f"위도와 경도가 추가된 새로운 파일이 생성되었습니다: {output_file_path}")