import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración de la página
st.set_page_config(page_title="Self-Discovery AI", page_icon="✨")
st.title("✨ Descubre tu Máximo Potencial")

# Inicializar historial de mensajes si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Interfaz lateral
api_key = st.sidebar.text_input("Introduce tu Gemini API Key:", type="password")
uploaded_file = st.sidebar.file_uploader("Sube una captura opcional 📸", type=["png", "jpg", "jpeg"])

# Mostrar mensajes previos del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Cuadro de chat (Siempre al final para que sea visible)
if prompt := st.chat_input("Escribe aquí tus canciones o lo que sientes..."):
    
    # Mostrar mensaje del usuario inmediatamente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4. Lógica de respuesta de la IA
    if not api_key:
        st.error("⚠️ Por favor, introduce tu API Key en la barra lateral para recibir respuesta.")
    else:
        try:
            # Configuración de conexión estable
            genai.configure(api_key=api_key, transport='rest')
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.chat_message("assistant"):
                with st.spinner("Analizando tu vibración..."):
                    # Preparar contenido
                    instruccion = "Eres un guía de potencial personal. Analiza la música del usuario."
                    contenido = [instruccion, f"Usuario: {prompt}"]
                    
                    if uploaded_file:
                        img = Image.open(uploaded_file)
                        contenido.append(img)
                    
                    # Generar respuesta
                    response = model.generate_content(contenido)
                    st.markdown(response.text)
                    
                    # Guardar respuesta en el historial
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        except Exception as e:
            st.error(f"Hubo un problema al procesar: {e}")
