#네이버 검색량 데이터를 분석함.
#밈의 진화단계
#1. 잠재: 상대 검색량이 1 미만
#2. 확산: 상대 검색량이 급격히 증가(기울기가 1 이상일 때부터 그래프가 최고점일 때까지)
#3. 절정: 상대 검색량이 급격한 증가 후 횡보, 최고치부터 그래프 상대 검색량이 50%일 때까지)
#4. 쇠퇴: 서서히 검색량이 감소하는 단계, 상대 검색량 50% 이후

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
date_array__ = []
current_date = start_date

i = 0
while current_date <= end_date:
    date_array[current_date.strftime('%Y-%m-%d')] = i
    date_array__.append(current_date.strftime('%Y-%m-%d'))
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


    #확산 단계의 시작
    threshold = 1.0
    first_point = None

    for i in range(len(gradient)):
        if gradient[i] > threshold:
            first_point = i
            break

    #절정 단계의 시작

    # 확산 단계 이후 그래프의 최고점
    threshold = 0.01
    peak_point = first_point
    if first_point != None:
        for i in range(first_point, len(gradient)):
            if smoothed_y[i] > smoothed_y[peak_point]:
                peak_point = i

        print('확산: ' + str(date_array__[first_point]) + ' ~ ' + str(date_array__[peak_point]))

    #쇠퇴 단계의 시작

    # 그래프의 상대량이 50이 되는 지점
    threshold = smoothed_y[peak_point]/2
    half_point = None

    if peak_point != None:
        for i in range(peak_point, len(gradient)):
            if smoothed_y[i] < threshold:
                half_point = i
                break

    # 그래프 그리기
    plt.plot(x, newData, label='Original')
    plt.plot(x, smoothed_y, label='Smoothed')
    plt.plot(x, gradient, label='Gradient')
    plt.plot(x, gradient_diff, label='Gradient Difference')
    if first_point != None:
        plt.scatter(x[first_point], smoothed_y[first_point], color='r', label='First Gradient = 1')
    if peak_point != None:
        plt.scatter(x[peak_point], smoothed_y[peak_point], color='g', label='First Gradient peak')
    if half_point != None:

        print('절정: ' + str(date_array__[peak_point]) + ' ~ ' + str(date_array__[half_point]))
        plt.scatter(x[half_point], smoothed_y[half_point], color='black', label='First 50%')

    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Period')
    plt.title(str(num) + ' meme graph')
    plt.show()

for i in range(1, 39):
    showsmoothgraph(i)