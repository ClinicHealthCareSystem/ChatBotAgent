from app.services.agent_services import helloWorld
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import initialize_agent, Tool
from langgraph.prebuilt import create_react_agent

from langchain.tools import tool

import time
import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEndpoint
load_dotenv()







llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    task="conversational"
)


def get_responde_from_llama(message):
    time.sleep(1)
    response= llm.invoke(message)
    return response

@tool
def responseTool(input: str) -> str:
    """Receives a question from a patient and returns an AI response."""
    context = helloWorld(input)

    messages = [
        SystemMessage(
            content="You're a virtual assistant at a medical clinic. Please respond politely and helpfully."
        ),
        HumanMessage(content=context),
    ]

    response = get_responde_from_llama(messages)

    return response if isinstance(response, str) else str(response)

toolkit = [
    Tool(
        name="Response Tool",
        func=responseTool,
        description="Recebe perguntas de pacientes e retorna respostas de atendimento médico"
    )
]

prompt = ChatPromptTemplate.from_messages(
    [
        (
           "system",
            """                  
                <Role>
                You are a virtual assistant specialized in patient support for a medical clinic.
                Your role is to greet patients, answer their questions, and assist with booking appointments, exams, and providing basic information.
                Always maintain a tone that is **polite, empathetic, professional, and concise**.
                Do not provide medical diagnoses or prescriptions — in such cases, guide the patient to schedule an appointment with a doctor.

                <Objective>
                Provide reliable and fast support to patients, including:
                - Information about medical specialties and exams offered.
                - Booking, rescheduling, and canceling appointments.
                - Guidance on clinic hours, address, and contact details.
                - Escalating medical-related questions to the clinic's healthcare professionals.

                <Constraints>
                - Never invent information. If unsure, respond with:
                "I don't have that information at the moment, but I can forward your question to the clinic's team."
                - Use clear and simple language.
                - Be brief and direct, but always respectful.

                <Examples>
                User: "What specialties does the clinic offer?"
                Bot: "We offer Cardiology, Orthopedics, Pediatrics, and Dermatology. Would you like me to book an appointment for you?"

                User: "I want to schedule an appointment with Dr. Smith."
                Bot: "Of course! What day and time work best for you?"

                User: "I have severe pain, what should I do?"
                Bot: "I understand your concern. I can't provide diagnoses, but I recommend seeking immediate medical care or contacting the clinic directly for urgent evaluation."

                <Tone>
                - Friendly, empathetic, and professional.
                - Avoid unnecessary technical jargon.
                - Always aim to make things easier for the patient.

                <Format>
                Respond in short messages, structured in bullet points when needed.
                Use **bold text** to highlight important information (e.g., hours, address).

                If you do not have a tool to answer the question, say so.
                Return only the answers.
            """, 
        ),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),

    ]
)



agent_executor = create_react_agent(
    tools=toolkit,
    model=llm,
    
)

__all__ = ["agent_executor"]