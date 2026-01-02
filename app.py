import streamlit as st
import google.generativeai as genai
from PIL import Image
import pytesseract
import numpy as np
from typing import List

# --- Configuración de la página
st.set_page_config(page_title="Self-Discovery AI (Embeddings)", page_icon="✨")
st.title("✨ Descubre tu Máximo Potencial (Embeddings + OCR)")

st.markdown("""
Analiza tus canciones favoritas mediante vectores para descubrir patrones o similitudes.
Escribe tus canciones favoritas o sube una captura de pantalla con títulos de canciones.
""")

# --- Configurar API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.warning("⚠️ Añade tu API Key en Streamlit Secrets con la clave GOOGLE_API_KEY")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key, transport="rest")

# --- Función para generar embeddings
def get_embedding(texts: List[str]):
    embeddings = []
    for t in texts:
        emb_response = genai.embeddings.create(
            model="embedding-gecko-001",
            input=t
        )
        embeddings.append(np.array(emb_response.data[0].embedding))
    return embeddings

# --- Función similitud coseno
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# --- Función OCR
def ocr_image(img: Image.Image):
    text = pytesseract.image_to_string(img, lang='spa')
    return text.strip()

# --- Entradas del usuario
col1, col2 = st.columns([2, 1])
with col1:
    song_input = st.text_area("Escribe tus canciones favoritas, separadas por comas")
with col2:
    uploaded_file = st.file_uploader("Sube una captura 📸", type=["png", "jpg", "jpeg"])

texts_to_analyze = []

# Tomar texto escrito por usuario
if song_input:
    texts_to_analyze.extend([s.strip() for s in song_input.split(",") if s.strip()])

# Tomar texto extraído de la imagen
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Imagen subida", width=200)
    ocr_text = ocr_image(img)
    if ocr_text:
        st.info(f"Texto detectado en la imagen: {ocr_text}")
        texts_to_analyze.extend([s.strip() for s in ocr_text.split("\n") if s.strip()])

# --- Procesar embeddings y similitud
if texts_to_analyze:
    try:
        embeddings = get_embedding(texts_to_analyze)
        st.success("✅ Embeddings generados!")

        st.subheader("Similitudes entre canciones")
        for i in range(len(texts_to_analyze)):
            for j in range(i+1, len(texts_to_analyze)):
                sim = cosine_similarity(embeddings[i], embeddings[j])
                st.write(f"**{texts_to_analyze[i]}** ↔ **{texts_to_analyze[j]}** → Similaridad: {sim:.2f}")

        st.subheader("Recomendaciones")
        for i, s in enumerate(texts_to_analyze):
            similarities = [cosine_similarity(embeddings[i], embeddings[j]) if i != j else -1 for j in range(len(texts_to_analyze))]
            if len(similarities) > 1:
                best_idx = np.argmax(similarities)
                st.write(f"Para **{s}**, canción más similar: **{texts_to_analyze[best_idx]}** (sim {similarities[best_idx]:.2f})")

    except Exception as e:
        st.error(f"Error generando embeddings: {e}")
