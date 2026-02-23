import streamlit as st
import requests
import json

# Настройка страницы
st.set_page_config(page_title="GitHub Copilot API Chat", page_icon="🤖")
st.title("💬 GitHub Models Chat")

# Боковая панель для настроек
with st.sidebar:
    st.header("Настройки")
    api_token = st.text_input("GitHub Token", type="password", help="Вставь сюда свой PAT токен")
    model_choice = st.selectbox("Выбери модель", ["gpt-4o", "gpt-4o-mini", "o1-mini"])
    st.info("Лимиты: 50 запр/день для GPT-4o, 150 для mini.")

# Инициализация истории чата
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение истории чата
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле ввода сообщения
if prompt := st.chat_input("Напиши что-нибудь..."):
    if not api_token:
        st.error("Пожалуйста, введи токен в боковой панели!")
        st.stop()

    # Добавляем сообщение пользователя в историю
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Запрос к API GitHub
    with st.chat_message("assistant"):
        placeholder = st.empty()  # Место для динамического текста
        full_response = ""

        url = "https://models.github.ai/inference/chat/completions"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {api_token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json"
        }
        data = {
            "model": model_choice,
            "messages": st.session_state.messages,
            "stream": True  # Включаем потоковую передачу
        }

        try:
            response = requests.post(url, headers=headers, json=data, stream=True)

            if response.status_code == 200:
                # Обработка потока данных
                for line in response.iter_lines():
                    if line:
                        # Убираем префикс "data: "
                        line_text = line.decode('utf-8')
                        if line_text.startswith("data: "):
                            line_text = line_text[6:]

                        if line_text == "[DONE]":
                            break

                        try:
                            chunk = json.loads(line_text)
                            if chunk['choices'][0]['delta'].get('content'):
                                content = chunk['choices'][0]['delta']['content']
                                full_response += content
                                placeholder.markdown(full_response + "▌")
                        except:
                            continue

                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            elif response.status_code == 429:
                st.error("Ошибка 429: Лимит запросов на сегодня исчерпан!")
            else:
                st.error(f"Ошибка {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"Произошла ошибка: {e}")