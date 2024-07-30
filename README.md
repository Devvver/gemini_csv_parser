# gemini_csv_parser
Парсер с помощью данных из csv с поддержкой формул и шаблонов

# Установка
pip install streamlit  

pip install pandas  

pip install -U google-generativeai  

Нужно получить кей от API GEMINI по ссылке  https://www.youtube.com/watch?v=J8ksL3oqqUE
и вставить в 
genai.configure(api_key="тут ваш ключ")
Важно - не все страны поддерживаются, используйте https://protonvpn.com . После подлючения смените страну которая подерживает Google API, список
https://ai.google.dev/gemini-api/docs/available-regions?hl=ru
Парсинг тоже должен быть под прокси, иначе будете получать или 400 или 429 ошибку!

Интерфейс
[<img src="https://github.com/Devvver/gemini_csv_parser/blob/main/999.png" width="50%">](https://github.com/Devvver/gemini_csv_parser/blob/main/999.png)




