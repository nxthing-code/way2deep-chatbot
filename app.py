import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Self-Discovery AI", page_icon="✨")
st.title("✨ Descubre tu Máximo Potencial")
st.markdown("""
Analiza tu vibración actual a través de la música.  
**Escribe tus canciones favoritas** o **sube una captura de pantalla** para descubrir tus fortalezas.
""")

# Configura la API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.warning("⚠️ Añade tu API Key en Streamlit Secrets como GOOGLE_API_KEY")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key, transport="rest")

# --- Modelo compatible hardcodeado
# Cambia esto solo si tu cuenta no tiene acceso
selected_model_name = "gemini-1.5-flash-001"
model = genai.GenerativeModel(selected_model_name)
st.sidebar.info(f"Usando modelo: {selected_model_name}")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de texto e imagen
col1, col2 = st.columns([2, 1])
with col1:
    user_input = st.chat_input("Escribe aquí tus canciones o pensamientos...")
with col2:
    uploaded_file = st.file_uploader("Sube una captura 📸", type=["png", "jpg", "jpeg"])

# Procesar la solicitud
if user_input or uploaded_file:
    content_text = user_input if user_input else "Aquí hay una imagen para analizar canciones."
    st.session_state.messages.append({"role": "user", "content": content_text})

    with st.chat_message("user"):
        st.markdown(content_text)
        if uploaded_file:
            st.image(uploaded_file, width=200)

    with st.chat_message("assistant"):
        with st.spinner("Analizando…"):
            instruction = (
                "Actúa como un guía de autoconocimiento. "
                "Analiza las canciones para identificar emociones, fortalezas y consejos."
            )
            contents = [instruction, content_text]

            if uploaded_file:
                img = Image.open(uploaded_file)
                contents.append(img)
                contents.append("Analiza los nombres de canciones en la imagen.")

            try:
                result = model.generate_content(contents)
                answer = result.text if hasattr(result, "text") else str(result)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as err:
                st.error(f"Error al generar contenido: {err}")
