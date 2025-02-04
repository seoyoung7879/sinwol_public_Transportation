
폴더명: no.1
1 요일별/시간대별 승하차 인원
- 요일별 승하차 인원(grouped bar): 요일 * 인원수 * 승차/하차
파일명: PassengerBoardingAndAlightingByWeekday
- 시간대별 승하차 인원(stacked bar): 시간대 * 인원수 * 승차/하차
파일명: passengerByTimePeriod
- 요일/시간대별 승차 인원(line): 시간대 * 인원수 * 요일
파일명: passengersByWeekdayAndTime_boarding
- 요일/시간대별 하차 인원(line): 시간대 * 인원수 * 요일
파일명:passengersByWeekdayAndTime_alighting

*html파일명은 각각 실행하는 파이썬 파일명과 일치합니다.

폴더명: no.2
2 노선별 일평균 승하차 인원
- 일평균 승차 인원 * 일평균 하차 인원 (scatter)

폴더명: no.3
3 정류장별 승하차 인원
- 정류장별 승차 인원(bar, sort by 인원수 desc): 정류장 * 승차인원
- 정류장별 하차 인원(bar, sort by 인원수 desc): 정류장 * 하차인원

폴더명: no.4
4 (버스정류장/지하철 point를 250m 격자에 매핑한 뒤) 주요 출도착지 시각화
- 신월동 출발 네트워크
- 신월동 도착 네트워크
pydeck_3D_network.py
결과는 html파일로 같이 저장되어 있습니다

- 파이차트: 신월동 출발,도착 네트워크의 도착지 인원수 기준: qgz파일

-전처리: 전처리한 파일 순서대로 파일명 뒤에 번호를 붙여놓았습니다.(순서:1-2-3-4)

컬럼정의서: bus_useage_grouped.csv(전처리된 파일)컬럼정의서 입니다. 나머지 파일들의 컬럼명은 명확하거나 해당 정의서와 같습니다. 