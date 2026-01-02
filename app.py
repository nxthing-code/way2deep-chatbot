import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1️⃣ Configuración de página
st.set_page_config(page_title="Self‑Discovery AI", page_icon="✨")
st.title("✨ Descubre tu Máximo Potencial")
st.markdown("""
Analiza tu vibración actual a través de la música.  
**Escribe tus canciones favoritas** o **sube una captura de pantalla** para descubrir tus fortalezas.
""")

# --- 2️⃣ Configuración de API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.warning("❗ Añade tu API Key en Streamlit Secrets con la clave GOOGLE_API_KEY")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key, transport="rest")

# --- 3️⃣ Intentar modelos disponibles hasta encontrar uno que funcione
st.sidebar.markdown("### 🔍 Buscando modelo compatible...")
model_names = [m.name for m in genai.list_models()]
compatible_model = None

for name in model_names:
    try:
        # Intentar una llamada de prueba con generateText
        test_model = genai.GenerativeModel(name)
        # Si funciona sin excepción, lo elegimos
        compatible_model = test_model
        selected_model_name = name
        break
    except Exception:
        continue

if not compatible_model:
    st.error("❌ No se encontró un modelo que funcione con generativeContent.")
    st.stop()

st.sidebar.success(f"Modelo seleccionado: {selected_model_name}")

# --- 4️⃣ Mostrar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5️⃣ Entradas del usuario
col1, col2 = st.columns([2, 1])
with col1:
    user_input = st.chat_input("Escribe aquí tus canciones o lo que sientes...")
with col2:
    uploaded_file = st.file_uploader("Sube una captura 📸", type=["png", "jpg", "jpeg"])

if user_input or uploaded_file:
    user_text = user_input if user_input else "Analiza esta imagen de mis canciones."
    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.chat_message("user"):
        st.markdown(user_text)
        if uploaded_file:
            st.image(uploaded_file, width=200)

    # --- 6️⃣ Generar respuesta con IA
    with st.chat_message("assistant"):
        with st.spinner("✨ Analizando tu mensaje…"):
            prompt_instruction = (
                "Actúa como un guía de autoconocimiento. Analiza las canciones "
                "para identificar estado emocional, fortalezas y consejos motivadores."
            )
            inputs_for_model = [prompt_instruction, user_text]

            if uploaded_file:
                img = Image.open(uploaded_file)
                inputs_for_model.append(img)
                inputs_for_model.append("Analiza los nombres en la imagen.")

            try:
                response = compatible_model.generate_content(inputs_for_model)
                text = response.text if hasattr(response, "text") else str(response)
                st.markdown(text)
                st.session_state.messages.append({"role": "assistant", "content": text})
            except Exception as e:
                st.error(f"Error generando contenido: {e}")
