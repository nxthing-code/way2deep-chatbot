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
            # --- SOLUCIÓN AL ERROR 404 ---
            # Forzamos el uso de la API v1 (estable) y el transporte REST
            genai.configure(api_key=api_key, transport='rest')
            
            # Usamos el nombre del modelo compatible con v1
            model = genai.GenerativeModel('gemini-1.0-pro')
            
            with st.chat_message("assistant"):
                with st.spinner("Interpretando tu sintonía musical..."):
                    instruccion = (
                        "Eres un experto en psicología musical. Analiza estas canciones "
                        "para identificar fortalezas y estado emocional. Tono inspirador."
                    )
                    
                    # Generar respuesta
                    response = model.generate_content([instruccion, prompt])
                    st.markdown(response.text)
                    
                    # Guardar en historial
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        except Exception as e:
            st.error(f"Error de conexión: {e}")
            st.info("Si el error persiste, intenta crear una API Key nueva en un 'New Project' dentro de AI Studio.")
