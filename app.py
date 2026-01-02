import streamlit as st
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Self-Discovery AI", page_icon="✨")
st.title("✨ Descubre tu Máximo Potencial")
st.markdown("Analiza tu vibración actual a través de las canciones que escribas.")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Entrada de datos
api_key = st.sidebar.text_input("Introduce tu Gemini API Key:", type="password")

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
        st.error("⚠️ Por favor, introduce tu API Key en la barra lateral.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Conectando con la sabiduría musical..."):
                # URL forzando la versión estable v1
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Actúa como un guía de autoconocimiento. Analiza estas canciones y dime las fortalezas y potencial del usuario: {prompt}"
                        }]
                    }]
                }
                
                try:
                    response = requests.post(url, json=payload)
                    data = response.json()

                    # Verificamos si Google devolvió un error de seguridad o de clave
                    if 'error' in data:
                        st.error(f"Google API Error: {data['error']['message']}")
                    elif 'candidates' in data and data['candidates'][0]['content']['parts'][0]['text']:
                        texto_ia = data['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(texto_ia)
                        st.session_state.messages.append({"role": "assistant", "content": texto_ia})
                    else:
                        st.warning("Google no pudo generar una respuesta. Intenta con otras canciones.")
                        st.write("Respuesta técnica para depurar:", data) # Esto nos dirá qué pasa realmente

                except Exception as e:
                    st.error(f"Error inesperado: {e}")
