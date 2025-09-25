import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv


load_dotenv()
token = os.getenv("HF_API_TOKEN")


client = InferenceClient(model="meta-llama/Llama-3.1-8B-Instruct", token=token)


def menu_escolha():
    return """
    1. Consulta Médica
    2. Exames
    3. Visualizar Agendamentos
    4. Dúvidas
    """


def resposta_chatbot(prompt: str):
    resposta = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}]
    )
    texto = resposta.choices[0].message.content
    return texto


def responseLLM(input: str):
    opcao = input
    response = atendimento_chatbot(opcao)
    return response


def atendimento_chatbot(opcao: str):
    match opcao:
        case "1":
            prompt = (
                "Você é um assistente de clínica médica. "
                "Ajude o paciente a agendar uma consulta de forma clara e educada."
            )

            return resposta_chatbot(prompt)
        case "2":
            prompt = (
                "Você é um assistente de clinica médica. "
                "Ajude o paciente a solicitar exames, explicando o processo de forma clara."
            )
            return resposta_chatbot(prompt)
        case "3":
            prompt = "Aqui estão os agendamentos cadastrados para o paciente:"
            return resposta_chatbot(prompt)
        case "4":
            prompt = (
                "Você é um assistente de clínica médica. "
                "Responda as dúvidas do paciente de forma clara, educada e profissional. "
                "Não forneça diagnósticos, apenas orientações gerais."
            )
            return resposta_chatbot(prompt)
        case __:
            return (
                "Opção inválida. Por favor, escolha uma das opções abaixo:"
                + menu_escolha()
            )


# if __name__ == "__main__":
#     while True:
#         print(menu_escolha())
#         opcao = input("Digite a opcao desejada ")
#         if opcao.lower() == "sair":
#             print("Encerrando o antendimento")
#             break
#         resposta = atendimento_chatbot(opcao)
#         print("Chatbot:", resposta)
