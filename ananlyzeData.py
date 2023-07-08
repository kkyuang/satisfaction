#네이버 검색량 데이터를 분석함.
#밈의 진화단계
#1. 잠재: 상대 검색량이 1 미만
#2. 확산: 상대 검색량이 급격히 증가
#3. 절정: 상대 검색량이 급격한 증가 후 횡보, 최고치
#4. 쇠퇴: 서서히 검색량이 감소하는 단계

import matplotlib.pyplot as plt
from openpyxl import load_workbook
from datetime import datetime, timedelta
import numpy as np
from scipy.signal import argrelmax
from scipy.ndimage import gaussian_filter1d
from scipy.signal import savgol_filter
from scipy.signal import find_peaks


# 엑셀 파일 로드
workbook = load_workbook('memeNaver.xlsx')


#날짜 배열 만들기
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 7, 7)

date_array = {}
current_date = start_date

i = 0
while current_date <= end_date:
    date_array[current_date.strftime('%Y-%m-%d')] = i
    current_date += timedelta(days=1)
    i+=1

#그래프 함수
def showgraph(num):
    # 시트 선택
    sheet = workbook[str(num)]

    data = [cell.value for cell in sheet['A'][1:] if cell.value is not None]
    dates = [cell.value for cell in sheet['B'][1:] if cell.value is not None]

    newData = [ 0 for a in range(len(date_array))]
    for j in range(len(dates)):
        newData[date_array[dates[j]]] = data[j]

    # 그래프 그리기
    x = range(1, len(newData) + 1)
    plt.plot(x, newData)
    plt.xlabel('Date')
    plt.ylabel('Period')
    plt.title(str(num) + ' meme graph')
    plt.show()

#부드러운 그래프
def showsmoothgraph(num):
    # 시트 선택
    sheet = workbook[str(num)]

    data = [cell.value for cell in sheet['A'][1:] if cell.value is not None]
    dates = [cell.value for cell in sheet['B'][1:] if cell.value is not None]

    newData = [ 0 for a in range(len(date_array))]
    for j in range(len(dates)):
        newData[date_array[dates[j]]] = data[j]
    # 그래프 그리기
    x = range(1, len(newData) + 1)

    # 필터링을 통해 부드러운 그래프 생성
    smoothed_y = savgol_filter(newData, window_length=30, polyorder=2)

    #변화율 계산

    # 데이터의 기울기 계산
    gradient = np.gradient(smoothed_y, x)

    # 기울기의 변화율 계산
    gradient_diff = np.gradient(gradient, x)

    # 변화율이 크게 증가하는 부분 찾기
    threshold = 0.1
    peaks = argrelmax(gradient_diff, order=5)[0]
    selected_peaks = peaks[gradient_diff[peaks] > threshold]

    # 그래프 그리기
    plt.plot(x, newData, label='Original')
    plt.plot(x, smoothed_y, label='Smoothed')

    plt.plot(x, gradient, label='Gradient')
    plt.plot(x, gradient_diff, label='Gradient Difference')

    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Period')
    plt.title(str(num) + ' meme graph')
    plt.show()

for i in range(1, 49):
    showsmoothgraph(i)