import pandas as pd
import pydeck as pdk

# 데이터 로드
df = pd.read_csv(r'data-20250122T010720Z-001\data\bus_usage_grouped.csv')

# 승객수 100 이상 데이터 필터링
filtered_data = df[df['승객수'] >= 100]

# 새로운 파일 2 로드 (신월동의 정류장 ID를 확인)
sinwol_stops = pd.read_csv(r'data-20250122T010720Z-001\data\sinwol_busstops.csv')  # 파일 2 경로

# 신월동 정류장 ID 목록 추출
sinwol_stops_ids = sinwol_stops['정류장ID'].tolist()

# 1. 신월동에서 출발한 데이터 (출발 정류장이 신월동 정류장에 해당하는 경우)
sinwol_departures = filtered_data[filtered_data['승차정류장ID'].isin(sinwol_stops_ids)]

# 2. 신월동으로 도착한 데이터 (도착 정류장이 신월동 정류장에 해당하는 경우)
sinwol_arrivals = filtered_data[filtered_data['하차정류장ID'].isin(sinwol_stops_ids)]

# 3. Pydeck ArcLayer를 이용한 3D 곡선 시각화 (출발한 경우)
# 초기 맵 설정
view_state = pdk.ViewState(
    latitude=sinwol_departures['위도_x'].mean(),  # 중심 위도
    longitude=sinwol_departures['경도_x'].mean(),  # 중심 경도
    zoom=12,  # 줌 레벨
    pitch=45  # 맵 기울기
)

# ArcLayer 생성 (출발한 경우)
arc_layer_departures = pdk.Layer(
    "ArcLayer",
    data=sinwol_departures,
    get_source_position=["경도_x", "위도_x"],  # 출발 위치
    get_target_position=["경도_y", "위도_y"],  # 도착 위치
    get_width="승객수 / 20",  # 곡선 두께 (승객수에 비례, 필요에 따라 조정)
    get_source_color=[255, 0, 0, 160],  # 출발점 색상 (빨간색, 투명도 포함)
    get_target_color=[0, 0, 255, 160],  # 도착점 색상 (파란색, 투명도 포함)
    pickable=True,  # 툴팁 활성화
    auto_highlight=True,  # 강조 효과
)

# 지도 구성 (출발한 경우)
deck_departures = pdk.Deck(
    layers=[arc_layer_departures],
    initial_view_state=view_state,
    tooltip={"text": "출발: {경도_x}, {위도_x}\n도착: {경도_y}, {위도_y}\n이동량: {승객수}"}
)

# 신월동에서 출발한 이동을 HTML로 저장
deck_departures.to_html("sinwol_departures_3d_network.html")

# 4. Pydeck ArcLayer를 이용한 3D 곡선 시각화 (도착한 경우)
# ArcLayer 생성 (도착한 경우)
arc_layer_arrivals = pdk.Layer(
    "ArcLayer",
    data=sinwol_arrivals,
    get_source_position=["경도_x", "위도_x"],  # 출발 위치
    get_target_position=["경도_y", "위도_y"],  # 도착 위치
    get_width="승객수 / 20",  # 곡선 두께 (승객수에 비례, 필요에 따라 조정)
    get_source_color=[0, 255, 0, 160],  # 출발점 색상 (초록색, 투명도 포함)
    get_target_color=[0, 0, 255, 160],  # 도착점 색상 (파란색, 투명도 포함)
    pickable=True,  # 툴팁 활성화
    auto_highlight=True,  # 강조 효과
)

# 지도 구성 (도착한 경우)
deck_arrivals = pdk.Deck(
    layers=[arc_layer_arrivals],
    initial_view_state=view_state,
    tooltip={"text": "출발: {경도_x}, {위도_x}\n도착: {경도_y}, {위도_y}\n이동량: {승객수}"}
)

# 신월동으로 도착한 이동을 HTML로 저장
deck_arrivals.to_html("sinwol_arrivals_3d_network.html")