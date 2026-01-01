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

# 2. Barra lateral para la API Key
api_key = st.sidebar.text_input("Introduce tu Gemini API Key:", type="password")
st.sidebar.info("Espacio de entretenimiento para el autoconocimiento.")

if api_key:
    try:
        # ✅ Configuración correcta (sin forzar REST)
        genai.configure(api_key=api_key)

        # ✅ Modelo válido y actualizado
        model = genai.GenerativeModel("gemini-1.5-flash-latest")

        # Inicializar historial del chat
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Mostrar mensajes previos
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 3. Zona de entrada: Texto e Imagen
        col1, col2 = st.columns([2, 1])
        with col1:
            prompt = st.chat_input("Escribe aquí tus canciones o lo que sientes...")
        with col2:
            uploaded_file = st.file_uploader("Sube una captura 📸", type=["png", "jpg", "jpeg"])

        # 4. Procesar la interacción
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
                        "Actúa como un guía de potencial personal y autoconocimiento. "
                        "Analiza las canciones para identificar el estado emocional, "
                        "fortalezas y cómo alcanzar el máximo potencial. "
                        "Tono motivador. No eres psicólogo. "
                        "Si hay imagen, lee los nombres de las canciones."
                    )

                    contenido_para_ia = [instruccion]

                    if prompt:
                        contenido_para_ia.append(f"El usuario dice: {prompt}")

                    if uploaded_file:
                        img = Image.open(uploaded_file)
                        contenido_para_ia.append(img)
                        contenido_para_ia.append(
                            "Estas son canciones del usuario. Analiza su energía emocional."
                        )

                    # ✅ Llamada correcta a Gemini
                    response = model.generate_content(contenido_para_ia)
                    st.markdown(response.text)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response.text
                    })

    except Exception as e:
        st.error(f"Error de conexión con Gemini: {e}")

else:
    st.warning("Introduce tu API Key en la barra lateral para comenzar.")
