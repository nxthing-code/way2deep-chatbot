import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Psico-IA Guía", page_icon="🧠")
st.title("🧠 Tu Guía Psicológico Personalizado")

# Aquí pedimos la "Llave" que guardaste en el Paso 1
api_key = st.sidebar.text_input("Pega aquí tu Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash')

    # Inicializar el historial del chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar mensajes previos
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Reaccionar a la entrada del usuario
    if prompt := st.chat_input("¿Qué te gustaría descubrir hoy sobre ti?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Respuesta de la IA
        with st.chat_message("assistant"):
            response = model.generate_content(f"Actúa como un psicólogo experto. El usuario dice: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("Por favor, introduce tu API Key en la barra lateral para comenzar.")
