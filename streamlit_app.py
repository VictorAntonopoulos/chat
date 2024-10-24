import streamlit as st
from openai import OpenAI

# Título personalizado do chatbot
st.title("💬 Chatbot Galdí")

# Acessar a chave da API de forma segura a partir do arquivo secrets.toml
openai_api_key = st.secrets["openai_api_key"]

# Criar um cliente OpenAI usando a chave correta
client = OpenAI(api_key=openai_api_key)

# Inicializar o estado de sessão para armazenar as mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir todas as mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de entrada para o usuário enviar mensagens
if prompt := st.chat_input("Digite sua mensagem:"):
    # Armazenar e exibir a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gerar uma resposta usando a API OpenAI
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Exibir a resposta em tempo real
    response = ""
    with st.chat_message("assistant"):
        for chunk in stream:
            response += chunk["choices"][0]["delta"].get("content", "")
            st.markdown(response)

    # Armazenar a resposta do assistente no estado de sessão
    st.session_state.messages.append({"role": "assistant", "content": response})
