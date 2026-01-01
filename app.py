import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración de la página
st.set_page_config(page_title="Self-Discovery AI", page_icon="✨")
st.title("✨ Descubre tu Máximo Potencial")
st.markdown("""
Analiza tu vibración actual a través de la música.  
**Escribe tus canciones favoritas** o **sube una captura de pantalla** para descubrir tus fortalezas.
""")

# 2. Barra lateral
api_key = st.sidebar.text_input("Introduce tu Gemini API Key:", type="password")
st.sidebar.info("Espacio de entretenimiento para el autoconocimiento.")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # ESTA ES LA LÍNEA CLAVE CORREGIDA:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 3. Entrada
        col1, col2 = st.columns([2, 1])
        with col1:
            prompt = st.chat_input("Escribe tus canciones o lo que sientes...")
        with col2:
            uploaded_file = st.file_uploader("Sube una captura 📸", type=["png", "jpg", "jpeg"])

        if prompt or uploaded_file:
            user_content = prompt if prompt else "Analiza esta captura de mis canciones."
            st.session_state.messages.append({"role": "user", "content": user_content})
            with st.chat_message("user"):
                st.markdown(user_content)
                if uploaded_file:
                    st.image(uploaded_file, width=200)

            with st.chat_message("assistant"):
                with st.spinner("Analizando tu sintonía..."):
                    instruccion = (
                        "Actúa como un guía de potencial personal. Analiza las canciones para identificar "
                        "el estado emocional, fortalezas y cómo alcanzar el máximo potencial. "
                        "Tono motivador y de entretenimiento. No eres psicólogo. Si hay imagen, lee las canciones."
                    )
                    contenido = [instruccion]
                    if prompt: contenido.append(f"Usuario: {prompt}")
                    if uploaded_file: contenido.extend([Image.open(uploaded_file), "Analiza esta imagen."])

                    response = model.generate_content(contenido)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Error de conexión: {e}")
else:
    st.warning("Introduce tu API Key para comenzar.")
