import pandas as pd
import spacy

df = pd.read_csv('rzn_ved2.csv')  # Датасет газеты

df = df.dropna().reset_index(drop=True)  # На всякий случай убираем все пустые ячейки
df = df.drop_duplicates().reset_index(drop=True)  # ... И все дубликаты

nlp = spacy.load("ru_core_news_sm")  # Загружаем русский корпус spacy для извлечения именованных сущностей из текста

l1 = []  # Список для слова
l2 = []  # Список метки этого слова. Например, персона, локация, организация

for i in range(len(df)):
    doc = nlp(df['text'][i])  # Загружаем текст статьи в модель 
    for ent in doc.ents:  # Ищём там именованные сущности
        l1.append(ent.text)
        l2.append(ent.label_)

df = pd.DataFrame({'name': l1, 'label': l2})  # Из полученных данных формируем датафрейм

df = df.loc[df['label'] == 'PER'].reset_index(drop=True)  # Ищём, кто из людей упоминался в текстах
df_sort = df['name'].value_counts(sort=True)  # Сортируем по количеству упоминаний 
print(df_sort.head())

df = df.loc[df['label'] == 'ORG'].reset_index(drop=True)  # Ищём, какие ведомства и организации упоминались в текстах
df_sort = df['name'].value_counts(sort=True)  # Сортируем по количеству упоминаний 
print(df_sort.head())
