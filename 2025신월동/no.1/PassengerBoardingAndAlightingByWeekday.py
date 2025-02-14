{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 요일별 승하차 인원 분석"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import plotly.express as px\n",
    "\n",
    "# CSV 파일 읽기\n",
    "bus_data = pd.read_csv('data-20250122T010720Z-001/data/sinwol_bus.csv')\n",
    "\n",
    "# 승차일시와 하차일시를 datetime 형식으로 변환\n",
    "bus_data['승차일시'] = pd.to_datetime(bus_data['승차일시'], format='%Y%m%d%H%M%S')\n",
    "bus_data['하차일시'] = pd.to_datetime(bus_data['하차일시'], format='%Y%m%d%H%M%S')\n",
    "\n",
    "# 요일 정보 추출 (0=월요일, 6=일요일)\n",
    "bus_data['승차요일'] = bus_data['승차일시'].dt.day_name()  # 요일명 추출\n",
    "bus_data['하차요일'] = bus_data['하차일시'].dt.day_name()  # 요일명 추출\n",
    "\n",
    "# 요일 순서를 설정\n",
    "ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']\n",
    "bus_data['승차요일'] = pd.Categorical(bus_data['승차요일'], categories=ordered_days, ordered=True)\n",
    "bus_data['하차요일'] = pd.Categorical(bus_data['하차요일'], categories=ordered_days, ordered=True)\n",
    "\n",
    "# 요일별 승차와 하차 인원수 집계 (observed=False 추가)\n",
    "boarding_counts = bus_data.groupby('승차요일', observed=False)['승객수'].sum().reset_index(name='승차인원수')\n",
    "alighting_counts = bus_data.groupby('하차요일', observed=False)['승객수'].sum().reset_index(name='하차인원수')\n",
    "\n",
    "# 요일별 승하차 인원 통합\n",
    "combined_counts = pd.merge(boarding_counts, alighting_counts, left_on='승차요일', right_on='하차요일', how='outer')\n",
    "\n",
    "# 시각화 (grouped bar로 승차와 하차 인원 나란히 비교)\n",
    "fig = px.bar(combined_counts, \n",
    "             x='승차요일', \n",
    "             y=['승차인원수', '하차인원수'], \n",
    "             title='요일별 승하차 인원',\n",
    "             labels={'value': '인원수', 'variable': '승하차'},\n",
    "             barmode='group',  # grouped bar 형식\n",
    "             color_discrete_sequence=['blue', 'red'])  # 승차는 파랑, 하차는 빨강\n",
    "\n",
    "# 특정 폴더 경로 지정\n",
    "output_path = 'no.1/PassengerBoardingAndAlightingByWeekday.html'\n",
    "\n",
    "# 그래프를 지정한 경로에 HTML 파일로 저장\n",
    "fig.write_html(output_path)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}