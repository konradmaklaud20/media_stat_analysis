import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px

df = pd.read_csv('rzn_ved2.csv')  # Датасет газеты

df = df.dropna().reset_index(drop=True)  # На всякий случай убираем все пустые ячейки
df = df.drop_duplicates().reset_index(drop=True)  # ... И все дубликаты

df['views'] = df['views'].apply(lambda x: int(x))  # Количество просмотров: преобразуем из строкового типа данных в целочисленный 

df['date_format'] = pd.to_datetime(df['date'], format='%Y-%m-%d')  # Форматируем дату в datetime
df1 = df['tag'].value_counts(sort=True)  # Сортируем рубрики по количеству встречаемости

df_sorted = df.sort_values("date_format", ascending=False).reset_index(drop=True)  # Сортируем по дате
d = df_sorted.groupby(["tag"])['views'].agg('sum')  # Группируем по рубрикам и считаем общую сумму просмотров по каждой
df = pd.concat([d, df1], axis=1)  # Объединяем два датафрейма

df['tags'] = df.index  # Формируем новую колонку с названиями рубрик
df_sorted = df.sort_values("tag", ascending=False).reset_index(drop=True)  # ... И сортируем её
df_sorted = df_sorted[:15]  # ... Для наглядности возьмём только 15 самых популярных 

d = {}  # Создаём словарь
for i in range(len(df_sorted)):  # ... Где key — название рубрики, value — среднее ежемесячное количество её просмотров
    d[df_sorted['tags'][i]] = df_sorted['views'][i] // df_sorted['tag'][i]
    
dfd = pd.DataFrame(d.items(), columns=['tag', 'mean'])  # Создаём новый датафрейм из словаря, указываем нужные названия колонок
dfd = dfd.sort_values("mean", ascending=False).reset_index(drop=True)  # Сортируем по популярности: от высокого к низкому

# Формируем слой графика
large_rockwell_template = dict(
layout = go.Layout(
    titlefont=dict(
        size=20,
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        title='Рубрика',
        titlefont=dict(
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Среднее количество просмотров',
        titlefont=dict(
            size=18,
            color='#7f7f7f'
        )

    )
)
)
# Формируем гистограмму
fig = px.histogram(dfd, x="tag", y='mean',
                   color_discrete_sequence=['rgb(226,83,221)'],
                   title='Среднее количество просмотров по рубрикам',
                   template=large_rockwell_template)

fig.update_xaxes(showgrid=False)  # Убираем отображение линий по оси X
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(153,153,255, 0.7)')  # Оставляем только отображение по оси Y
fig.update_layout(hovermode="x", xaxis=dict(title='Рубрика'), yaxis=dict(title='Среднее количество просмотров'))  # Тип отображения данных при наведении мышки, заголовок и название оси
fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
)
fig.update(layout=dict(title=dict(x=0.5)))  # Располагаем заголовок по центру 
div = plotly.io.to_html(fig, full_html=False, config=dict(displayModeBar=False))  # Преобразуем график для отображения на веб-странице
