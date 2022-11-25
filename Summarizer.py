# графическая библиотека
import tkinter as tk
import nltk  # пакет библиотек и программ для обработки естественного языка
from textblob import TextBlob  # библиотека для анализа тональности текста
from newspaper import Article  # библиотека для загрузки и парсинга статей

nltk.download('punkt')  # используем nltk для установки модели
# строка используется только во время первой компиляции затем она не нужна

# функция для чтения URL статьи а затем ее загрузки и парсинга
# в ней также прописан анализ тональности текста и вывод данных в текстовые поля
def summarize():
    # получаем введенную пользователем URL и записываем ее в переменную
    url = utext.get('1.0', "end").strip()
    article = Article(url)
    # загружаем статью
    article.download()
    # парсим статью
    article.parse()
    # вызываем метод для обработки скачанной статьи
    article.nlp()

    # для того чтобы вывести в текстовые поля полученные данные нам нужно их разблокировать
    title.config(state='normal')
    author.config(state='normal')
    publication.config(state='normal')
    summary.config(state='normal')
    sentiment.config(state='normal')

    # работаем с текстовыми полями
    # удаляем из них старый текст и вставляем новый
    # заголовок
    title.delete('1.0', 'end')  # удаляем предыдущий текст от начала до конца строки
    title.insert('1.0', article.title)  # с начала строки вставляем новый текст полученный методами article.parse() и article.nlp()

    # автор
    author.delete('1.0', 'end')
    author.insert('1.0', article.authors)

    # дата публикации
    publication.delete('1.0', 'end')
    publication.insert('1.0', article.publish_date)

    # краткое содержание
    summary.delete('1.0', 'end')
    summary.insert('1.0', article.summary)

    # удаляем предыдущие результаты анализа тональности текста потом проводим новый анализ
    # выводим его результаты в текстовое поле
    # используем библиотеку TextBlob и находим тональность текста для несокращенного текста
    # если вставить в метод summary то мы получим тональность текста для краткого содержания
    analysis = TextBlob(article.text)
    sentiment.delete('1.0', 'end')  # удаляем старые данные из текстового поля
    # вставляем в поле сам анализ в виде числа а потом выводим тон словом для того чтобы пользователю было понятно
    # если анализ больше нуля то тон положительный если нет то тон отрицательный
    # если же положительных и отрицательных слов поровну или мнение в статье не отражается то результат нейтральный
    sentiment.insert('1.0', f'Polarity: {analysis.polarity}, '
                            f'Sentiment: {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}')
    # данные в текстовые поля были введены так что их можно закрыть
    # это делается для того чтобы пользователь не смог в них ничего написать
    title.config(state='disabled')
    author.config(state='disabled')
    publication.config(state='disabled')
    summary.config(state='disabled')
    sentiment.config(state='disabled')


# построение интерфейса
root = tk.Tk()  # конструктор самого окна
root.title("Краткое содержание статей")  # заголовок
root.geometry('1200x600')  # задаем размеры окну

tlabel = tk.Label(root, text="Заголовок")  # создание текстовой метки с помощью виджета Label
tlabel.pack()  # использование одного из менеджеров геометрии а именно упаковщика(packer)
# используется для отображения текстовой метки в окне
title = tk.Text(root, height=1, width=140)  # создание многострочного текстового поля и регуляция его размера
# с помощью метода config задаем фон и блокируем доступ пользователя к текстовому полю
title.config(state='disabled', bg='#dddddd')
title.pack()  # отображаем текстовое поле

# повторяем процесс для автора
alabel = tk.Label(root, text="Автор(ы)")
alabel.pack()
author = tk.Text(root, height=1, width=140)
author.config(state='disabled', bg='#dddddd')
author.pack()

# повторяем процесс для даты публикации
plabel = tk.Label(root, text="Дата публикации")
plabel.pack()
publication = tk.Text(root, height=1, width=140)
publication.config(state='disabled', bg='#dddddd')
publication.pack()

# повторяем процесс для поля в котором будет отражаться краткое содержание
slabel = tk.Label(root, text="Краткое содержание")
slabel.pack()
summary = tk.Text(root, height=20, width=140)
summary.config(state='disabled', bg='#dddddd')
summary.pack()

# повторяем процесс для поля в котором отображается резкльтат анализа тональности текста
selabel = tk.Label(root, text="Анализ тональности текста")
selabel.pack()
sentiment = tk.Text(root, height=1, width=140)
sentiment.config(state='disabled', bg='#dddddd')
sentiment.pack()

# создание метки и текстового поля для ввода URL пользователем
# с этим полем взаимодействует пользователь так что блокировку доступа не ставим
ulabel = tk.Label(root, text="URL")
ulabel.pack()
utext = tk.Text(root, height=1, width=140)
utext.pack()

# кнопка для запуска процесса сокращения текста
btn = tk.Button(root, text="Сократить", command=summarize)  # создаем кнопку с помощью виджета Button
# присваиваем ей текст и команду
btn.pack()  # отображаем кнопку

root.mainloop()  # функция запускающая цикл обработки событий
# без нее окно не будет реагировать на внешние раздражители
