import pandas as pd
import plotly
import plotly.graph_objs as go

df = pd.read_csv('rzn_ved2.csv')  # Датасет газеты

df = df.dropna().reset_index(drop=True)  # На всякий случай убираем все пустые ячейки
df = df.drop_duplicates().reset_index(drop=True)  # ... И все дубликаты

df['views'] = df['views'].apply(lambda x: int(x))  # Количество просмотров: преобразуем из строкового типа данных в целочисленный 

df['date_format'] = pd.to_datetime(df['date'], format='%Y-%m-%d')  # Форматируем дату в datetime
df['date_y_m'] = df['date_format'].dt.strftime('%Y-%m')  # Выбираем шаг: по месяцам  

df_sorted = df.sort_values("date_y_m", ascending=False).reset_index(drop=True)  # Сортируем даты
d = df_sorted.groupby(["date_y_m"])['views'].agg('sum')  # Группируем просмотры по дате, считаем общую сумму просмотров за каждый месяц
df = pd.DataFrame(d)  # Создаём новый датафрейм
df['date_y_m'] = df.index  # Заносим в него колонку с датой

# Формируем график
trace = go.Scatter(
    x=df['date_y_m'],
    y=df['views'],
    mode='lines',
    line=dict(width=3, shape='spline', smoothing=1.3),
    fillcolor='rgba(0,100,80,0.2)',
    marker=dict(
        color='rgb(226,83,221)',
        size=202,
        line=dict(
            color='MediumPurple',
            width=2,
            colorscale="Cividis",
        )
    ),
)

# Добавляем слой с указанием заголовка, названиями осей
layout = go.Layout(
    title='<b>Статистика просмотров материалов<br>«Рязанских ведомостей» по месяцам</b>'.format('П'),
    titlefont=dict(
        size=20,
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        title='Дата',
        titlefont=dict(
            # family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Суммарное количество просмотров',
        titlefont=dict(
            # family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )

    )
)

fig = go.Figure(data=[trace], layout=layout)  # Собираем всё в один график
fig.update_xaxes(showgrid=False)  # Убираем отображение линий по оси X
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(153,153,255, 0.7)')  # Оставляем только отображение по оси Y
fig.update_layout(hovermode="x")  # Тип отображения данных при наведении мышки 
# Указываем, как именно будут отображаться данные при наведении 
fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
)
fig.update(layout=dict(title=dict(x=0.5)))  # Располагаем заголовок по центру 
div = plotly.io.to_html(fig, full_html=False, config=dict(displayModeBar=False))  # Преобразуем график для отображения на веб-странице
