import streamlit as st
from openai import OpenAI

# ============================================
# CONFIGURACIÓN (cambía solo la API Key)
# ============================================
API_KEY = st.secrets.get("GROQ_API_KEY", "clave-de-respaldo-solo-local")# <--- PONÉ TU CLAVE DE GROQ
BASE_URL = "https://api.groq.com/openai/v1"
MODELO = "llama-3.3-70b-versatile"

# Configuración de la página
st.set_page_config(page_title="Mi Asistente IA", page_icon="🤖", layout="centered")

# Ocultar el menú de Streamlit para que se vea profesional
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Inicializar el cliente
cliente = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Título
st.title("🤖 Asistente Virtual")
st.caption("Preguntame lo que quieras, estoy aquí para ayudarte.")

# Inicializar el historial en la sesión (para que no se borre al recargar)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! ¿En qué te ayudo?"}]

# Mostrar todos los mensajes del historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input del usuario
if prompt := st.chat_input("Escribí tu mensaje..."):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Obtener respuesta del bot
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Preparar el historial para la API
                api_messages = [{"role": "system", "content": "Eres un asistente amable y útil."}]
                for m in st.session_state.messages:
                    api_messages.append({"role": m["role"], "content": m["content"]})
                
                respuesta = cliente.chat.completions.create(
                    model=MODELO,
                    messages=api_messages,
                    temperature=0.7,
                )
                reply = respuesta.choices[0].message.content
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")