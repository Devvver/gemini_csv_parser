import streamlit as st
import google.generativeai as genai
import pandas as pd
import re
import os

# Настройка API-ключа
genai.configure(api_key="AIzaSyADZzyXuCCDeQUx-bUUGmIfl7M32REyBW4")

# Инициализация модели
model = genai.GenerativeModel('models/gemini-pro')
# Возможен вызов других моделей, пример  model = genai.GenerativeModel(model_name="gemini-1.5-flash")

st.title("Генерация контента с помощью Google Generative AI")
st.write("Загрузите CSV файл и получите результаты.")

# Поле для загрузки файла
uploaded_file = st.file_uploader("Загрузите CSV файл", type="csv")

if uploaded_file is not None:
    # Чтение загруженного файла
    df = pd.read_csv(uploaded_file)

    # Приведение заголовков к нижнему регистру
    df.columns = df.columns.str.lower()

    # Создание нового столбца 'result' для хранения результатов
    df['result'] = ''

    # Поле для ввода Memo
    memo_template = st.text_area("Введите шаблон prompt (для названий столбцов используйте [[]]):",
                                 "")


    clean_text = st.checkbox("Очистить ответ от лишних символов", value=True)
    st.write(f"Используется в том случае, если вы хотите получить результат в виде html кода.")

    def replace_placeholders(template, row):
        """Заменяет плейсхолдеры вида [[...]] в шаблоне на значения из строки DataFrame."""

        def replacer(match):
            column_name = match.group(1).lower()  # Игнорируем регистр
            return str(row[column_name])

        return re.sub(r'\[\[(.*?)\]\]', replacer, template)


    def clean_response(response_text):
        """Удаляет лишние символы в начале и в конце строки."""
        return response_text.strip("`").strip("```html").strip("```")


    def gemini_get_data(text):
        try:
            response = model.generate_content(text)
            if clean_text:
                return clean_response(response.text)
            else:
                return response.text
        except Exception as e:
            st.error(f"Произошла ошибка: {str(e)}")
            return None



    if st.button("Запустить"):
        progress_bar = st.progress(0)
        table_placeholder = st.empty()
        status_text = st.empty()

        total_rows = len(df)


        for i, row in df.iterrows():
            # Подставляем значения из строки в шаблон Memo
            formatted_text = replace_placeholders(memo_template, row)
            result = gemini_get_data(formatted_text)
            df.at[i, 'result'] = result

            # Обновление прогресса и таблицы

            progress_bar.progress((i + 1) / total_rows,
                                  text=f"Парсится {i + 1} строка из {total_rows}")
            table_placeholder.dataframe(df)

        # Завершение процесса и показ полной таблицы
        st.success("Процесс завершен!")

        script_directory = os.path.dirname(os.path.abspath(__file__))
        output_file_path = os.path.join(script_directory, "result.csv")

        try:
            df.to_csv(output_file_path, index=False)
            st.write(f"Файл с результатами сохранен как {output_file_path}.")
        except Exception as e:
            st.error(f"Ошибка при сохранении файла: {str(e)}")
