import streamlit as st
from groq import Groq

# 1. Configuración de la página
st.set_page_config(page_title="Self-Discovery AI", page_icon="✨")
st.title("✨ Descubre tu Máximo Potencial")
st.markdown("Analiza tu vibración actual a través de la música (Vía Groq Cloud).")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Barra lateral para la API Key de Groq
# Recuerda: Aquí debes pegar la clave que empieza por "gsk_..."
api_key = st.sidebar.text_input("Introduce tu Groq API Key:", type="password")

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Lógica del Chat
if prompt := st.chat_input("Escribe tus canciones favoritas..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:
        st.error("⚠️ Por favor, introduce tu API Key de Groq en la barra lateral.")
    else:
        try:
            # Inicializar el cliente de Groq
            client = Groq(api_key=api_key)
            
            with st.chat_message("assistant"):
                with st.spinner("Groq está analizando tu sintonía..."):
                    # Llamada al modelo Llama 3 (uno de los mejores y más rápidos)
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": "Eres un experto en psicología musical y potencial personal. Analiza las canciones del usuario para identificar fortalezas y estado emocional. Tono motivador e inspirador."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                    )
                    
                    texto_ia = completion.choices[0].message.content
                    st.markdown(texto_ia)
                    st.session_state.messages.append({"role": "assistant", "content": texto_ia})

        except Exception as e:
            st.error(f"Error al conectar con Groq: {e}")
            st.info("Asegúrate de que tu clave empieza por 'gsk_'")
