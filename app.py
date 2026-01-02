import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Self-Discovery AI", page_icon="✨")
st.title("✨ Descubre tu Máximo Potencial")
st.markdown("Analiza tu vibración actual a través de las canciones que escribas.")

# Inicializar historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Barra lateral para la API Key
api_key = st.sidebar.text_input("Introduce tu Gemini API Key:", type="password")

# Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Cuadro de chat
if prompt := st.chat_input("Escribe aquí tus canciones favoritas..."):
    
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:
        st.error("⚠️ Introduce tu API Key en la barra lateral.")
    else:
        try:
            # CONFIGURACIÓN UNIVERSAL: Usamos gemini-pro (el más estable)
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            with st.chat_message("assistant"):
                with st.spinner("Interpretando tu sintonía musical..."):
                    # Instrucciones simplificadas
                    instruccion = (
                        "Eres un experto en psicología musical y potencial personal. "
                        "Analiza las siguientes canciones escritas por el usuario para identificar "
                        "sus fortalezas y estado emocional actual. Tono inspirador."
                    )
                    
                    # Generar respuesta
                    response = model.generate_content([instruccion, prompt])
                    st.markdown(response.text)
                    
                    # Guardar en historial
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        except Exception as e:
            st.error(f"Error de conexión: {e}")
            st.info("Nota: Si aparece error 404, prueba a generar una nueva API Key en Google AI Studio.")
