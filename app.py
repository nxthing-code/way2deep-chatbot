import streamlit as st
import google.generativeai as genai
from PIL import Image

# =====================================================
# CONFIGURACIÓN DE GEMINI (API KEY DESDE STREAMLIT CLOUD)
# =====================================================
# ⚠️ NO pegues aquí tu API Key
# Streamlit la lee automáticamente desde Settings → Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# =========================
# CONFIGURACIÓN DE LA PÁGINA
# =========================
st.set_page_config(page_title="Self-Discovery AI", page_icon="✨")

st.title("✨ Descubre tu Máximo Potencial")
st.markdown("""
Analiza tu vibración actual a través de la música.  
**Escribe tus canciones favoritas** o **sube una captura de pantalla**  
para descubrir tus fortalezas y tu estado emocional.
""")

st.sidebar.info("Espacio de entretenimiento para el autoconocimiento.")

# =========================
# MODELO GEMINI
# =========================
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# =========================
# HISTORIAL DEL CHAT
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# ENTRADA DE TEXTO E IMAGEN
# =========================
col1, col2 = st.columns([2, 1])

with col1:
    prompt = st.chat_input("Escribe aquí tus canciones o lo que sientes...")

with col2:
    uploaded_file = st.file_uploader(
        "Sube una captura 📸",
        type=["png", "jpg", "jpeg"]
    )

# =========================
# PROCESAR INTERACCIÓN
# =========================
if prompt or uploaded_file:

    user_message = prompt if prompt else "Analiza esta imagen con mis canciones."
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)
        if uploaded_file:
            st.image(uploaded_file, width=200)

    with st.chat_message("assistant"):
        with st.spinner("Analizando tu sintonía..."):

            instruccion = (
                "Actúa como un guía de autoconocimiento y desarrollo personal. "
                "Analiza las canciones para identificar el estado emocional, "
                "fortalezas internas y posibles caminos de crecimiento. "
                "Tono motivador y positivo. No eres psicólogo. "
                "Si hay una imagen, lee los nombres de las canciones."
            )

            contenido_para_ia = [instruccion]

            if prompt:
                contenido_para_ia.append(f"El usuario dice: {prompt}")

            if uploaded_file:
                imagen = Image.open(uploaded_file)
                contenido_para_ia.append(imagen)
                contenido_para_ia.append(
                    "Estas son canciones del usuario. Analiza su energía emocional."
                )

            # 🔮 Llamada a Gemini
            response = model.generate_content(contenido_para_ia)

            st.markdown(response.text)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text
            })
