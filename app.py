import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Self-Discovery AI", page_icon="✨")
st.title("✨ Descubre tu Máximo Potencial")

api_key = st.sidebar.text_input("Introduce tu Gemini API Key:", type="password")

if api_key:
    try:
        # 1. Usamos transporte 'rest' para evitar protocolos v1beta problemáticos
        genai.configure(api_key=api_key, transport='rest')
        
        # 2. Intentamos el nombre directo sin 'models/'
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Escribe tus canciones favoritas...")
        uploaded_file = st.sidebar.file_uploader("Sube una captura", type=["png", "jpg"])

        if prompt or uploaded_file:
            # Lógica de respuesta igual a la anterior...
            # (Mantén el resto de tu lógica de procesamiento aquí)
            pass

    except Exception as e:
        # Si el 404 persiste, mostramos una lista de lo que TU llave sí puede ver
        st.error(f"Error: {e}")
        if "404" in str(e):
            st.info("Intentando buscar modelos alternativos disponibles para tu cuenta...")
            modelos = [m.name for m in genai.list_models()]
            st.write("Modelos disponibles detectados:", modelos)
else:
    st.warning("Introduce tu API Key para comenzar.")
