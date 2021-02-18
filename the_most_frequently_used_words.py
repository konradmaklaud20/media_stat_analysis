import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

df = pd.read_csv('rzn_ved2.csv')  # Датасет газеты

df = df.dropna().reset_index(drop=True)  # На всякий случай убираем все пустые ячейки
df = df.drop_duplicates().reset_index(drop=True)  # ... И все дубликаты

def clean_text(text, stop_words):
  """
  Функция для предобработки текста 
  """
  text = [word for word in text.split() if word not in stop_words]
  text = ' '.join(text)
  return text


stop_words_2 = stopwords.words("russian")  # Загружаем корпус русских стоп-слов
stop_words_1 = [i.capitalize() for i in stop_words_2]  # Дополняем его теми же словами, но с заглавной буквы
stop_words = stop_words_1 + stop_words_2  # Объединяем оба списка

# df['title'], если находим самые часто используемые слова в заголовках. df['text'], если в текстах
df['title'] = df.apply(lambda x: clean_text(x['title'], stop_words), axis=1)  # Применяем функцию clean_text
spec_chars = string.punctuation + '\n\xa0«»\t—…'  # Создаём переменную с различными знаками пунктуации

text = ''
# df['title'], если находим самые часто используемые слова в заголовках. df['text'], если в текстах
for i in df['title']:  # Соединяем все заголовки в одну строку
  text += i + ' '

text = "".join([ch for ch in text if ch not in spec_chars])  # Удаляем знаки пунктуации и спецсимволы
text_tokens = word_tokenize(text)  # Разбиваем текст на токены
text1 = nltk.Text(text_tokens)  # Строим корпус из текста
fdist = FreqDist(text1)  # Строим словарь встречаемости слов

most_common_title = list(fdist.most_common(30))  #  Показываем 30 самых популярных слов


wc = WordCloud(max_words=500, width=1920, margin=10, height=1080, background_color="white").generate(text)  # Строим облако слов
plt.imshow(wc, interpolation="bilinear")  # Отрисовываем
plt.show()  # Показываем
