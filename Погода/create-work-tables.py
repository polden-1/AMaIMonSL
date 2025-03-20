import pandas as pd
from openpyxl import Workbook

hours = 12

df_start = pd.read_excel('исходная_таблица.xlsx', engine='openpyxl', skiprows=6)

df_start['Дата'] = pd.to_datetime(df_start['Местное время в Москве (ВДНХ)'], format='%d.%m.%Y %H:%M')

фильтр = (
    (df_start['Дата'].dt.month >= 2) &
    (df_start['Дата'].dt.month <= 5) &
    ~((df_start['Дата'].dt.month == 5) & (df_start['Дата'].dt.day > 10))
)

df = df_start.loc[фильтр, ['Дата', 'T']]

wb = Workbook()
ws = wb.active
ws.append(["год", "месяц", "декада", "номер декады", "температура"])


for year in range(2014, 2025):
    counter = 0
    for month in range(2, 6):
        for decade in range (1, 4):
            counter += 1
            
            decade_start = (decade - 1) * 10
            decade_end = decade * 10
            if decade == 3:
                decade_end += 1
            
            фильтр = (
                (df['Дата'].dt.year == year) &
                (df['Дата'].dt.month == month) &
                (df['Дата'].dt.day > decade_start) & 
                (df['Дата'].dt.day <= decade_end) &
                (df['Дата'].dt.hour == hours)
            )
            
            df_filtered = df.loc[фильтр, ['Дата', 'T']]
            
            if not df_filtered.empty:
                mid = round(df_filtered['T'].mean(), 4)
                ws.append([year, month, decade, counter, mid])

wb.save('температура-по-декадам.xlsx')

wb = Workbook()
ws = wb.active
ws.append(["декада", "температура"])


decade_start = 0
decade_end = 10

фильтр = (
    (df['Дата'].dt.year == 2025) &
    (df['Дата'].dt.month == 2) &
    (df['Дата'].dt.day > decade_start) & 
    (df['Дата'].dt.day <= decade_end) &
    (df['Дата'].dt.hour == hours)
)

df_filtered = df.loc[фильтр, ['Дата', 'T']]
if not df_filtered.empty:
            mid = round(df_filtered['T'].mean(), 4)
            ws.append([1, mid])
    
wb.save('температура-февраль-2025.xlsx')