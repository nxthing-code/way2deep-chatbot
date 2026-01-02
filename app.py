import streamlit as st
from groq import Groq

# 1. Configuración de la página
st.set_page_config(page_title="Self-Discovery AI", page_icon="✨")
st.title("✨ Descubre tu Máximo Potencial")
st.markdown("---")

# 2. Gestión de la API Key mediante Secrets
# Asegúrate de haber configurado 'GROQ_API_KEY' en el panel de Secrets de Streamlit
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("⚠️ No se encontró la API Key en los Secrets de Streamlit.")
    st.stop()

# Inicializar historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Barra Lateral (Sidebar)
with st.sidebar:
    st.header("Opciones")
    # Botón para limpiar el chat
    if st.button("🗑️ Limpiar Conversación"):
        st.session_state.messages = []
        st.rerun()
    
    st.info("""
    **Cómo funciona:**
    Escribe las canciones que más escuchas hoy y la IA analizará tus fortalezas actuales.
    """)

# 4. Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Lógica del Chat
if prompt := st.chat_input("Escribe aquí tus canciones o cómo te sientes..."):
    
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Inicializar el cliente de Groq con la clave de los Secrets
        client = Groq(api_key=api_key)
        
        with st.chat_message("assistant"):
            with st.spinner("Interpretando tu sintonía musical..."):
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Eres un experto en psicología musical y potencial personal. "
                                "Tu objetivo es analizar las canciones que el usuario mencione "
                                "para identificar sus fortalezas, su estado emocional y darle "
                                "un consejo motivador para alcanzar su máximo potencial hoy."
                            )
                        },
                        {"role": "user", "content": prompt}
                    ],
                )
                
                texto_ia = completion.choices[0].message.content
                st.markdown(texto_ia)
                st.session_state.messages.append({"role": "assistant", "content": texto_ia})

    except Exception as e:
        st.error(f"Hubo un error al procesar tu solicitud: {e}")
