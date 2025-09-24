from app.services.agent_services import helloWorld
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

import time
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_name="gpt-4o-mini", api_key=api_key, temperature=0)


def get_response_from_open_ai(message):
    time.sleep(1)
    response = llm.invoke(message)
    return response


@tool
def responseTool(question: str) -> str:
    """Receives a question from a patient and returns an AI response."""

    context = helloWorld(question)

    messages = [
        SystemMessage(
            content="You're a virtual assistant at a medical clinic. Please respond politely and helpfully."
        ),
        HumanMessage(content=context),
    ]

    response = get_response_from_open_ai(messages)
    return response.content if hasattr(response, "content") else str(response)


toolkit = [responseTool]

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
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

agent = create_openai_tools_agent(llm, toolkit, prompt)
agent_executor = AgentExecutor(agent=agent, tools=toolkit, verbose=True)

__all__ = ["agent_executor"]
