import pandas as pd

# Загружаем файл
df = pd.read_excel('исходная_таблица.xlsx', engine='openpyxl', skiprows=6)

df['Дата'] = pd.to_datetime(df['Местное время в Москве (ВДНХ)'], format='%d.%m.%Y %H:%M')

фильтр = (
    (df['Дата'].dt.month >= 2) &
    (df['Дата'].dt.month <= 5) &
    ~((df['Дата'].dt.month == 5) & (df['Дата'].dt.day > 10))
)

df_filtered = df.loc[фильтр, ['Дата', 'T']]
df_filtered.to_excel('температура_февраль_май.xlsx', index=False)
