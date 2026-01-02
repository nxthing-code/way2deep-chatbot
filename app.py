import streamlit as st
import google.generativeai as genai
from PIL import Image

# ===============================
# CONFIGURACIÓN DE GEMINI
# ===============================
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# ===============================
# CONFIGURACIÓN DE LA PÁGINA
# ===============================
st.set_page_config(page_title="Self-Discovery AI", page_icon="✨")

st.title("✨ Descubre tu Máximo Potencial")
st.markdown("""
Analiza tu vibración actual a través de la música.  
Escribe tus canciones favoritas o sube una captura de pantalla.
""")

st.sidebar.info("Espacio de entretenimiento para el autoconocimiento.")

# ✅ MODELO CORRECTO (CON VISIÓN)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# ===============================
# HISTORIAL
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===============================
# ENTRADAS
# ===============================
col1, col2 = st.columns([2, 1])

with col1:
    prompt = st.chat_input("Escribe aquí tus canciones o lo que sientes...")

with col2:
    uploaded_file = st.file_uploader(
        "Sube una captura 📸",
        type=["png", "jpg", "jpeg"]
    )

# ===============================
# PROCESAMIENTO
# ===============================
if prompt or uploaded_file:

    user_text = prompt if prompt else "Analiza esta imagen con mis canciones."
    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.chat_message("user"):
        st.markdown(user_text)
        if uploaded_file:
            st.image(uploaded_file, width=200)

    with st.chat_message("assistant"):
        with st.spinner("Analizando tu sintonía..."):

            instruccion = (
                "Actúa como un guía de autoconocimiento. "
                "Analiza las canciones para identificar el estado emocional "
                "y fortalezas internas. Tono motivador. No eres psicólogo."
            )

            if uploaded_file:
                image = Image.open(uploaded_file)
                contenido_para_ia = [instruccion, image]
            else:
                contenido_para_ia = [f"{instruccion}\n\nUsuario: {prompt}"]

            response = model.generate_content(contenido_para_ia)

            st.markdown(response.text)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text
            })
