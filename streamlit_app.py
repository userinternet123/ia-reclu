import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = Ollama(model="llama3.1:latest")

def main():
    st.title("Chat con Alexus")
    
    # Entrada del nombre del bot
    bot_name = st.text_input("Tu asistente virtual", value="Alexus")
    
    # Define el prompt para el cliente
    prompt = f'Hola, soy {bot_name}, tu asistente virtual de selección y contratación de personal para {bot_name}. ¿En qué puedo ayudarte hoy?'
    
    # Define el prompt para el servidor
    prompt_server = f"""Hola, soy {bot_name}, tu asistente virtual de selección y contratación de personal para {bot_name}.
    Empresa: Alexus
    Dirección:    Departamento de Escuintla
    Función del chat bot:  recopilar información de los candidatos para las plazas disponibles, como nombre, correo electrónico, número de teléfono, experiencia laboral y habilidades.
    Función del chat bot:  hacer preguntas clave para evaluar si el candidato cumple con los requisitos básicos del puest.
    Función del chat bot: coordinar y agendar entrevistas con los candidatos preseleccionados.
    Con las siguientes plazas disponibles:
Especialista de Información Comercial
Descripción del puesto:
- Preparar y estructurar bases de datos de valor para la toma de decisiones comerciales estratégicas según lineamientos y requerimientos del área.
- Elaborar Informes Gerenciales u otro tipo de informe según requerimiento.
Beneficios: Prestaciones de ley.
Funciones del puesto:
- Asegurar la estructuración y delimitación de las bases de datos de información comercial estratégica, según requerimientos del jefe inmediato.
Habilidades y conocimientos requeridos:
- Alto conocimiento en Alteryx, Microsoft office y Python
- Inglés avanzado o intermedio (conversación, escritura, lectura, comprensión)
- Experiencia en Matemática y Estadística Aplicada.
PILOTO DE TRASLADO DE MAQUINARIA
Descripción del puesto
Conducir el traslado de maquinaria de acuerdo a procedimientos y seguridad ocupacional
Funciones del puesto
Revisar el cabezal y remolque de plataforma baja, previo a la conducción, para evitar que se dañen, aplicar procedimientos previos establecidos, seguridad y cuidado de los recursos.
Beneficios
Capacitación Constante
Prestaciones adicionales a las de la Ley
Auxilio Póstumo 
Habilidades y conocimientos
•Graduado de diversificado o técnico.
•Mínimo 2 años de experiencia en puestos similares.
•Licencia tipo A vigente.
OPERADOR DE MAQUINARIA (área de Maquinaria de Cultivo)
Descripción del puesto
Operar la maquinaria agrícola para realizar labores de adecuación, preparación de suelos, levantamiento de la plantación, aplicación de agroinsumos, siembra y resiembra semi-mecanizada de acuerdo con los requerimientos de la programación del área.
Funciones del puesto
    Verificación del área de trabajo, estado físico y el funcionamiento de la maquinaria de acuerdo con lineamientos de inspección,
    Operar la maquinaria agrícola según características, requerimientos del área y normas de seguridad.
Beneficios
•Prestaciones adicionales a las de la ley.
•Capacitación constante.
Habilidades y conocimientos
Genéricas
    Comunicación
    Trabajo en equipo
    Servicio al cliente
 Técnicas
    Conocer el funcionamiento de la maquinaria agrícola
    Conocimiento en labores de cultivo( Labores de adecuación de suelo, preparación de suelos , levantamientos de la plantación, labores varias, aplicación de agroinsumos, siembra y resiembra semi-mecanizada.
 Deseable
    Conocimientos de seguridad industrial
    Conocimientos en maquinaria agrícola
    Disponibilidad de horarios
    Licencia tipo E Vigente.
"""
    
    # Muestra el prompt del bot en la interfaz del cliente
    st.text_area("Descripción del bot", value=prompt, height=150, key="client_prompt", disabled=True)
    
    # Inicializa el historial del chat si no está en el estado de sesión
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Configura el prompt de la conversación
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_server),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )
    chain = prompt_template | llm
    
    # Entrada del usuario para la conversación
    user_input = st.text_input("Inicia tu conversación", key="user_input") 
        
    if st.button("Enviar"):
        if user_input.lower() == "salir":
            st.session_state["chat_history"].append(HumanMessage(user_input))
            st.session_state["chat_history"].append(AIMessage("¡Hasta luego!"))
            st.stop()
        else:
            response = chain.invoke({"input": user_input, "chat_history": st.session_state["chat_history"]})
            st.session_state["chat_history"].append(HumanMessage(user_input))
            st.session_state["chat_history"].append(AIMessage(response))
    
    # Muestra el historial del chat
    chat_display = "" 
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):
            chat_display += f"Tu: {msg.content}\n"
        else:
            chat_display += f"{bot_name}: {msg.content}\n"

    st.text_area("Chat", value=chat_display, height=400, key="chat_display", disabled=True)

if __name__ == "__main__":
    main()
