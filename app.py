import streamlit as st
from openai import OpenAI

# ============================================
# CONFIGURACIÓN (cambía solo la API Key)
# ============================================
API_KEY = st.secrets.get("GROQ_API_KEY", "clave-de-respaldo-solo-local")# <--- PONÉ TU CLAVE DE GROQ
BASE_URL = "https://api.groq.com/openai/v1"
MODELO = "llama-3.3-70b-versatile"


# ==========================================================
# CONFIGURACIÓN DE LA APP
# ==========================================================
st.set_page_config(page_title="BurgerBot 🍔", page_icon="🍔", layout="centered")

# ==========================================================
# 🎨 ESTILOS CSS MODERNOS (NEON / GLASSMORPHISM)
# ==========================================================
st.markdown("""
<style>
    /* Fondo con gradiente dinámico estilo neón */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
    }
    /* Contenedor principal con efecto cristal */
    .main > div {
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(12px);
        border-radius: 30px;
        padding: 25px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
    }
    /* Tarjetas de chat (glassmorphism) */
    .stChatMessage {
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(8px);
        border-radius: 20px !important;
        border: 1px solid rgba(255,255,255,0.08);
        padding: 16px 20px !important;
        margin: 12px 0 !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        transition: all 0.2s ease;
    }
    .stChatMessage:hover {
        border-color: rgba(255,107,107,0.3);
        box-shadow: 0 8px 30px rgba(255,107,107,0.1);
    }
    /* Mensaje del usuario (gradiente caliente) */
    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(238,90,36,0.3);
    }
    /* Mensaje del asistente (oscuro con borde) */
    .stChatMessage[data-testid="assistant"] {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        color: #f0f0f0 !important;
    }
    /* Input de texto con estilo neón */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.07) !important;
        border: 2px solid rgba(255,107,107,0.4) !important;
        border-radius: 40px !important;
        color: white !important;
        padding: 16px 22px !important;
        font-size: 16px !important;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(255,107,107,0.05);
    }
    .stTextInput > div > div > input:focus {
        border-color: #ff6b6b !important;
        box-shadow: 0 0 35px rgba(255,107,107,0.2);
    }
    /* Títulos con efecto neón */
    h1, h2, h3, .stTitle {
        color: white !important;
        text-shadow: 0 0 30px rgba(255,107,107,0.15);
        font-weight: 700 !important;
    }
    /* Subtítulos y texto secundario */
    .stCaption, .stMarkdown p {
        color: rgba(255,255,255,0.7) !important;
    }
    /* Ocultar elementos de Streamlit */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    /* Botón de limpiar chat (lo agregamos más abajo) */
    .stButton button {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 30px !important;
        color: white !important;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: rgba(255,107,107,0.2) !important;
        border-color: #ff6b6b !important;
        box-shadow: 0 0 25px rgba(255,107,107,0.15);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# CONFIGURACIÓN DE LA API (GROQ)
# ==========================================================
API_KEY = st.secrets.get("GROQ_API_KEY", "clave-local-de-prueba")
BASE_URL = "https://api.groq.com/openai/v1"
MODELO = "llama-3.3-70b-versatile"

cliente = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ==========================================================
#  PROMPT (El "cerebro" del bot)
# ==========================================================
SISTEMA_PROMPT = """
Eres un asistente virtual profesional y amable. Tu trabajo es ayudar a los clientes con sus consultas de forma clara, rápida y eficiente.

🎯 REGLAS OBLIGATORIAS:
1. Saludá con calidez y ofrecé ayuda.
2. Preguntá el nombre del cliente y su consulta principal.
3. Si el cliente pide información, respondé con claridad y ofrecé alternativas.
4. Si el cliente quiere comprar algo, pedí los detalles necesarios (producto, cantidad, etc.).
5. Si el cliente quiere agendar un turno, pedí fecha y hora preferida.
6. Si no sabés algo, decí: "Te voy a derivar con un asesor en breve" y no inventes información.
7. Siempre ofrecé ayuda adicional al final de cada respuesta.

🎨 ESTILO DE RESPUESTA:
- Usá un tono cálido y profesional.
- Usá emojis para dar calidez 😊📅🛍️✅.
- Respondé de forma clara y concisa (máximo 150 palabras).
- Si el cliente se despide, agradecé y ofrecé seguimiento.

📌 EJEMPLOS DE CONVERSACIÓN:
Cliente: "Hola"
Tú: "¡Hola! 😊 ¿Cómo estás? Soy tu asistente virtual. Decime, ¿en qué puedo ayudarte hoy?"

Cliente: "Quiero información sobre sus servicios"
Tú: "¡Claro! Para poder darte la mejor información, ¿me decís tu nombre y qué tipo de servicio te interesa?"

Cliente: "Quiero hacer un pedido"
Tú: "¡Perfecto! 📦 Para tomar tu pedido, necesito que me digas qué producto querés, la cantidad y tus datos de contacto. ¿Me los pasas?"
"""

# ==========================================================
# FUNCIÓN PARA CHATEAR CON EL BOT
# ==========================================================
st.session_state.messages = [
    {"role": "assistant", "content": "👋 ¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?"}
]

# Mostrar mensajes anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input del usuario
if prompt := st.chat_input("Escribí tu pedido o consulta..."):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Obtener respuesta del bot
    with st.chat_message("assistant"):
        with st.spinner("🍔 Preparando tu pedido..."):
            try:
                # Construir el historial completo para la API
                api_messages = [{"role": "system", "content": SISTEMA_PROMPT}]
                for m in st.session_state.messages:
                    api_messages.append({"role": m["role"], "content": m["content"]})
                
                response = cliente.chat.completions.create(
                    model=MODELO,
                    messages=api_messages,
                    temperature=0.7,
                )
                reply = response.choices[0].message.content
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")

# ==========================================================
# BOTÓN PARA LIMPIAR EL CHAT (opcional)
# ==========================================================
if st.button("🧹 Limpiar conversación"):
    st.session_state.messages = [
        {"role": "assistant", "content": "🍔 ¡Hola! Soy BurgerBot, tu asistente para pedidos. ¿Qué hamburguesa te tienta hoy? 😊"}
    ]
    st.rerun()