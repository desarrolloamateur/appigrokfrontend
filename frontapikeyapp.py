from groq import Groq
import streamlit as st

client = Groq(api_key="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")

def get_ai_response(messages):
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
        stream=True,
    )
    response = "".join(chunk.choices[0].delta.content or "" for chunk in completion)
    return response

def submit():
    user_input = st.session_state.user_input
    if user_input.lower() == 'exit':
        st.write("Gracias por chatear!! ¡Adiós!")
        st.stop()

    st.session_state['messages'].append({"role": "user", "content": user_input})

    with st.spinner("Obteniendo respuesta...."):
        ai_response = get_ai_response(st.session_state['messages'])
        st.session_state['messages'].append({"role": "assistant", "content": ai_response})

    st.session_state.user_input = ""

def chat():
    st.title("Chat con Llama 3.1")
    st.write("Bienvenido a este chat de IA! Escribe 'exit' para terminar la conversación.")

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    for message in st.session_state['messages']:
        role = "Tu" if message["role"] == "user" else "Bot"
        st.write(f"**{role}:** {message['content']}")

    with st.form(key='chat_form', clear_on_submit=True):
        st.text_input("Tu:", key="user_input")
        st.form_submit_button(label='Enviar', on_click=submit)

if __name__ == "__main__":
    chat()
