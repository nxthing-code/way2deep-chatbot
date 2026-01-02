import streamlit as st
import requests

st.set_page_config(page_title="Self-Discovery AI", page_icon="✨")
st.title("✨ Descubre tu Máximo Potencial")

# 1. Entrada de datos
api_key = st.sidebar.text_input("Introduce tu Gemini API Key:", type="password")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tus canciones favoritas..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:
        st.error("Introduce la API Key")
    else:
        # CONEXIÓN DIRECTA POR HTTP (Evita el error 404)
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": f"Analiza estas canciones para mi potencial personal: {prompt}"}]}]
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()
            
            # Extraer respuesta
            texto_ia = data['candidates'][0]['content']['parts'][0]['text']
            
            with st.chat_message("assistant"):
                st.markdown(texto_ia)
                st.session_state.messages.append({"role": "assistant", "content": texto_ia})
        except Exception as e:
            st.error(f"Error: Revisa que tu API Key sea correcta. (Detalle: {e})")
