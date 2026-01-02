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
        # Configuración técnica: Usamos transporte REST para evitar errores 404
        genai.configure(api_key=api_key, transport='rest')
        
        # Modelo oficial capaz de leer texto e imágenes sin librerías extra
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 3. Zona de entrada
        col1, col2 = st.columns([2, 1])
        with col1:
            prompt = st.chat_input("Escribe aquí tus canciones o lo que sientes...")
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
                        "Actúa como un guía de potencial personal. Analiza la música "
                        "para identificar estado emocional y fortalezas. Tono motivador. "
                        "No eres psicólogo. Si hay imagen, lee los nombres de las canciones."
                    )

                    # Preparar contenido (Multimodal)
                    contenido = [instruccion]
                    if prompt: 
                        contenido.append(f"Usuario dice: {prompt}")
                    if uploaded_file:
                        img = Image.open(uploaded_file)
                        contenido.append(img)
                        contenido.append("Lee las canciones de esta imagen y relaciónalas con el potencial del usuario.")

                    response = model.generate_content(contenido)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Error de conexión: {e}")
else:
    st.warning("Introduce tu API Key en la barra lateral para comenzar.")
