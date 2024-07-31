# gemini_csv_parser
Парсер с помощью данных из csv с поддержкой формул и шаблонов

# Установка
pip install streamlit  

pip install pandas  

pip install -U google-generativeai  

Нужно получить кей от API GEMINI , пример получения в видео  https://www.youtube.com/watch?v=J8ksL3oqqUE
и вставить в 
genai.configure(api_key="тут ваш ключ")
Важно - не все страны поддерживаются, используйте https://protonvpn.com . После подключения смените страну которая подерживает Google API, список
https://ai.google.dev/gemini-api/docs/available-regions?hl=ru
Парсинг тоже должен быть под прокси, иначе будете получать или 400 или 429 ошибку!

Интерфейс  

[<img src="https://github.com/Devvver/gemini_csv_parser/blob/main/999.png" width="50%">](https://github.com/Devvver/gemini_csv_parser/blob/main/999.png)  

1) Загружаем файл csv ( в кодировке UTF-8)
2) Пишем условие (prompt) для выполнения. Подерживаются заголовки из csv [[]], например
"Если размер [[Размер страницы ]] больше 100 кб тогда пишем статью по запросу [[h1]]".
Где [[Размер страницы ]] - столбцы которые есть в таблице и содержат данные.

3) После выполнения всех запросов результат сохранится в result.csv

На практике Google не рекомендует делать запросы чаще 1 раза в секунду (хотя поддерживает 600 запросов в минуту), через прокси редко когда получается делать чаще.
Тем не менее в случае проблем с количеством запросов добавьте задержку на 1 секунду.

По любым вопросам по скрипту пишите https://t.me/devvver
Могу спарсить данные, доделать под ваши нужды (за отдельную плату)







