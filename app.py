import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1️⃣ Configuración de la página
st.set_page_config(page_title="Self-Discovery AI", page_icon="✨")
st.title("✨ Descubre tu Máximo Potencial")
st.markdown("""
Analiza tu vibración actual a través de la música.  
**Escribe tus canciones favoritas** o **sube una captura de pantalla** para descubrir tus fortalezas.
""")

# 2️⃣ Barra lateral para la API Key
st.sidebar.info("Espacio de entretenimiento para el autoconocimiento.")

# Configura tu API Key
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport="rest")
else:
    st.warning("Introduce tu API Key en Secrets para continuar.")

# Modelo seguro y compatible
model = genai.GenerativeModel('text-bison-001')

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3️⃣ Zona de entrada: Texto e Imagen
col1, col2 = st.columns([2, 1])
with col1:
    prompt = st.chat_input("Escribe aquí tus canciones o lo que sientes...")
with col2:
    uploaded_file = st.file_uploader("Sube una captura 📸", type=["png", "jpg", "jpeg"])

# 4️⃣ Procesar la interacción
if prompt or uploaded_file:
    user_content = prompt if prompt else "Analiza esta captura de mis canciones."
    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user"):
        st.markdown(user_content)
        if uploaded_file:
            st.image(uploaded_file, width=200)

    # Respuesta de la IA
    with st.chat_message("assistant"):
        with st.spinner("Analizando tu sintonía..."):
            instruccion = (
                "Actúa como un guía de potencial personal y autoconocimiento. "
                "Analiza las canciones para identificar el estado emocional, "
                "fortalezas y cómo alcanzar el máximo potencial. Tono motivador. "
                "No eres psicólogo. Si hay imagen, lee los nombres de las canciones."
            )

            contenido_para_ia = [instruccion]
            if prompt:
                contenido_para_ia.append(f"El usuario dice: {prompt}")
            if uploaded_file:
                img = Image.open(uploaded_file)
                contenido_para_ia.append(img)
                contenido_para_ia.append("Analiza las canciones de esta imagen.")

            try:
                # Generar respuesta
                response = model.generate_content(contenido_para_ia)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error al generar contenido: {e}")
