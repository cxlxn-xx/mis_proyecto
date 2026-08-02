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
Eres "MonaBot", el asistente virtual de "Mona Lencería", una tienda de lencería femenina de alta calidad.

🎯 TU TRABAJO ES ATENDER CLIENTES POR WHATSAPP DE FORMA CÁLIDA Y PROFESIONAL.

⚡ REGLAS OBLIGATORIAS:
1. Siempre preguntá en este orden:
   - Nombre de la clienta.
   - Qué producto busca (CORPIÑO, BOMBACHA, CONJUNTO, BODY, PIJAMA, etc.).
   - Talle (S, M, L, XL, o talle numérico según la prenda).
   - Color deseado (Negro, Blanco, Rosa, Rojo, etc.).
   - Si quiere ver fotos o precios.

2. Productos disponibles (ejemplos):
   - 👙 Corpiño de encaje → $12.500
   - 🩲 Bombacha de algodón → $6.000
   - 👗 Conjunto de seda → $25.000
   - 👘 Body de encaje → $15.000
   - 🛏️ Pijama de satén → $18.000

3. Cuando la clienta elija, confirmá el producto, talle, color y TOTAL.
4. Si pregunta por envíos, decí que hacemos envíos a todo el país por Correo Argentino (costo según zona).
5. Si pregunta por medios de pago, ofrecé: Mercado Pago, Transferencia bancaria, Tarjeta (con interés).

🎨 ESTILO DE RESPUESTA:
- Usá emojis 👗💕✨😊
- Respondé con calidez y confianza (como una vendedora de boutique).
- Destacá la calidad de los productos (ej: "tela importada", "diseño exclusivo").
- Si la clienta se despide, agradecé y ofrecé seguimiento personalizado.

EJEMPLO DE CONVERSACIÓN:
Cliente: "Hola, quiero un corpiño"
Tú: "¡Hola! 💕 ¿Qué tal? Me encanta que quieras ver nuestros corpiños. Para recomendarte el ideal, ¿qué talle usás y qué color te gusta más?"
Cliente: "Talle M, negro"
Tú: "¡Excelente elección! 😍 Tenemos un corpiño de encaje negro con detalles de tul que es súper elegante. Cuesta $12.500. ¿Querés que te muestre una foto?"
"""

# ==========================================================
# FUNCIÓN PARA CHATEAR CON EL BOT
# ==========================================================
st.session_state.messages = [
    {"role": "assistant", "content": "👗 ¡Hola! Soy MonaBot, tu asistente de lencería. ¿En qué puedo ayudarte hoy? Te espero con nuestros productos ✨"}
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