from groq import Groq
import streamlit as st

client = Groq(api_key="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")

# Función para obtener la respuesta de la IA
def get_ai_response(messages):
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
        stream=True,
    )

    # Unir las respuestas del modelo en una sola cadena
    response = "".join(chunk.choices[0].delta.content or "" for chunk in completion)
    return response

# Función de chat
def chat():
    st.title("Chat con Llama 3.1")
    st.write("Bienvenido a este chat de IA! Escribe 'exit' para terminar la conversación.")

    # Estado de las conversaciones
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Formulario para enviar mensajes
    with st.form(key='chat_form', clear_on_submit=True):
        # Entrada de texto del usuario
        user_input = st.text_input("Tu:", key="user_input")
        submit_button = st.form_submit_button(label='Enviar')

        # Si se presiona el botón de enviar
        if submit_button:
            if user_input.lower() == 'exit':
                st.write("Gracias por chatear!! ¡Adiós!")
                return  # Termina la función de chat y detiene el flujo

            # Agregar mensaje del usuario a la conversación
            st.session_state['messages'].append({"role": "user", "content": user_input})

            with st.spinner("Obteniendo respuesta...."):
                ai_response = get_ai_response(st.session_state['messages'])
                # Agregar la respuesta de la IA
                st.session_state['messages'].append({"role": "assistant", "content": ai_response})

            # Limpiar el campo de entrada
            st.session_state.user_input = ""

            # Mostrar toda la conversación
            for message in st.session_state['messages']:
                role = "Tu" if message["role"] == "user" else "Bot"
                st.write(f"**{role}:** {message['content']}")

# Ejecutar la función de chat si el script es ejecutado directamente
if __name__ == "__main__":
    chat()
