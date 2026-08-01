import os
from openai import OpenAI


# Configuración para Groq
API_KEY = st.secrets.get("GROQ_API_KEY", "clave-de-respaldo-solo-local")
BASE_URL = "https://api.groq.com/openai/v1"
MODELO = "llama-3.3-70b-versatile"  # Un modelo potente y rápido

cliente = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Historial (la memoria del bot)
historial = [
    {"role": "system", "content": "Eres un asistente amable y servicial."}
]

def preguntar(mensaje):
    # 1. Agregamos el mensaje del usuario
    historial.append({"role": "user", "content": mensaje})
    
    # 2. Llamamos a la NUEVA API de Respuestas (la que muestra la web)
    respuesta = cliente.responses.create(
        model=MODELO,
        instructions="Eres un asistente amable y servicial.",
        input=historial,  # Le pasamos TODO el historial
        temperature=0.7,
        max_output_tokens=500,
    )
    
    # 3. Extraemos el texto de la respuesta
    msg_bot = respuesta.output_text
    historial.append({"role": "assistant", "content": msg_bot})
    return msg_bot

if __name__ == "__main__":
    print("\n🤖 Chatbot (V4-Flash) activado. Escribí 'salir' para terminar.\n")
    while True:
        user = input("Tú: ")
        if user.lower() == "salir":
            break
        try:
            print(f"Bot: {preguntar(user)}\n")
        except Exception as e:
            print(f"Error: {e}")
            print("Revisá tu saldo en la sección Billing de la web de DeepSeek.")