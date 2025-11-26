# import os
# from huggingface_hub import InferenceClient
# from dotenv import load_dotenv
# import json
# import re
# from typing import Dict, Any, Optional

# load_dotenv()
# token = os.getenv("HF_API_TOKEN")

# client = InferenceClient(model="meta-llama/Llama-3.1-8B-Instruct", token=token)


# PACIENTE_ID = 1

# SYSTEM_PROMPT = """
# Você é um assisten virtual de uma clínica médica chamda Sáude Mania.
# Seu objetivo é ajudar pacientes de forma educada, clara e profissional em portugês do Brasil.

# Faça perguntas claras e objetivas.
# """

# def detectar_opcao_menu(texto: str) -> Optional[int]:
#     texto = texto.strip()

#     if texto in ["1", "2", "3", "4"]:
#         return int(texto)

#     texto_lower = texto.lower()
#     if any(palavra in texto_lower for palavra in ["consulta", "agendar consulta","marcar consulta"]):
#         return 1
#     elif any(palavra in texto_lower for palavra in ["enxame", "agendar enxame","marcar enxame"]):
#         return 2
#     elif any(palavra in texto_lower for palavra in ["agendamento", "ver agendamentos","meus agendamentos"]):
#         return 3
#     elif any(palavra in texto_lower for palavra in ["dúvidas", "ajuda"]):
#         return 4
    
#     return None
    
# def dados_consulta(texto: str) -> Dict:
#     dados = {}

#     especialidade ={
#         "clínico geral": ["clínico", "clinico", "geral", "clínica geral"],
#         "pediatria": ["pediatr", "criança", "crianca", "infantil"],
#         "geriatria": ["geriatra", "geriatri", "velho", "idoso","geriatr"]
#     }
#     texto_lower = texto.lower()
#     for espec, palavras in especialidade.items():
#         if any(p in texto_lower for p in palavras):
#             dados["especialidades"] = espec
#             break
    
#     match_data = re.search(r'(\d{1,2})[/-](\d{1,2})(?:[/-](\d{4}))?', texto)
#     if match_data:
#         dia, mes, ano = match_data.groups()
#         ano = ano or "2025"
#         dados["data"] = f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"

#     match_hora = re.search(r'(\d{1,2})[h:](\d{2})?', texto)
#     if match_hora:
#         hora = match_hora.group(1).zfill(2)
#         minuto = match_hora.group(2) or "00"
#         dados["hora"] = f"{hora}:{minuto}"
    
#     if any(palavra in texto_lower for palavra in ["sim",  "confirmar", "ok", "correto", "isso", "confirmo"]):
#         dados["confirmado"] = True

#     return dados

# def dados_exames(texto: str) -> Dict:
#     dados = {}

#     tipos_enxames ={
#         "hemograma completo": ["hemograma","enxame de sangue", "sangue completo"],
#         "raio x": ["raio-x", "raio x", "rx"],
#     }

#     texto_lower = texto.lower()
#     for espec, palavras in tipos_enxames.items():
#         if any(p in texto_lower for p in palavras):
#             dados["tipos_enxames"] = espec
#             break

#     match_data = re.search(r'(\d{1,2})[/-](\d{1,2})(?:[/-](\d{4}))?', texto)
#     if match_data:
#         dia, mes, ano = match_data.groups()
#         ano = ano or "2025"
#         dados["data"] = f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"

#     match_hora = re.search(r'(\d{1,2})[h:](\d{2})?', texto)
#     if match_hora:
#         hora = match_hora.group(1).zfill(2)
#         minuto = match_hora.group(2) or "80"
#         dados["hora"] = f"{hora}:{minuto}"
    
#     if any(palavra in texto_lower for palavra in ["sim",  "confirmar", "ok", "correto", "isso", "confirmo"]):
#         dados["confirmado"] = True

#     return dados

# def llm(prompt: str) -> str:
    
#         resposta = client.chat.completions.create(
#             messages=[
#                  {"role": "system", "content": SYSTEM_PROMPT},
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         return resposta.choices[0].message.content.strip()

# ############
# def consulta(user_input: str, contexto: Dict) -> tuple[str, Dict]:
    
#     dados = dados_consulta(user_input, contexto)
#     contexto["dados"] = dados

#     falta_especialidade = "especialidade" not in dados
#     falta_data = "data" not in dados
#     falta_hora = "hora" not in dados

#     if falta_especialidade:
#         prompt = f"""O usuário quer agendar uma consulta e disse: "{user_input}"

#     Pergunte qual especialidade médica ele precisa de forma natural e amigável.
#     Mencione algumas opções como: cardiologia, dermatologia, clínico geral, pediatria, ortopedia."""
#         resposta = llm(prompt)
#         contexto["etapa"] = "coletantado_especialidade"
#         return resposta, contexto
#     elif falta_data:
#         prompt: f"""O usuário quer agendar consulta de {dados['especialidade']} e disse: "{user_input}"

# Pergunte que data ele prefere, de forma natural. Sugira que informe no formato DD/MM/AAAA."""
        
#         resposta = llm(prompt)
#         contexto["etapa"] = "coeltando_data"
#         return resposta, contexto
#     elif falta_hora:
#         resultado_tool = consultas_tool(
#             acao="buscar_disponiveis",
#             paciente_id=1,
#             especilidade=dados["especialidade"],
#             data=dados["data"]
#         )
#         contexto["etapa"] = "coletando_hora"
#         return resultado_tool, contexto
    
#     else:
#         if dados.get("confirmado"):
#             resultado_tool = consultas_tool(
#                 acao="agendar",
#                 paciente_id=1,
#                 especialidade=dados["especialidade"],
#                 data=dados["data"],
#                 hora=dados["hora"]                        
#                 )

#                 contexto["etapa"] = "concluido"
#                 contexto["dados"] = {}
#                 return resultado_tool, contexto
#         else:
#             from datetime import datetime
#             data_formada = datetime.strptime(dados["data"], "%Y-%m-%d").strftime("%d/%m/%Y")

#             confirmacao = f""" Vou confirmar os dados: 
#             📋 **Sua consulta:**
#             • Especialidade: {dados['especialidade'].title()}
#             • Data: {data_formatada}
#             • Horário: {dados['hora']}

#             Posso confirmar o agendamento? (Digite "sim" para confirmar)
#             """
#                 contexto["etapa"] = "confirmado"
#                 return confirmacao, contexto
#       ##################################################  
# def enxame(user_input: str, contexto: Dict) -> tuple[str, Dict]:
    
#     dados = dados_exames(user_input, contexto)
#     contexto["dados"] = dados

    
#     falta_tipo = "tipo_enxame" not in dados
#     falta_data = "data" not in dados

#     if falta_tipo:
        
#         resposta_tool = exames_tool(
#             acao="tipos_disponiveis",
#             paciente_id=1
#         )
#         contexto["etapa"] = "coletando_tipo"
#         return resultado_tool + "\n\nQual exame você precisa fazer?", contexto
    
#     elif falta_data:
#         prompt: f"""O usuário quer agendar enxame de {dados['especialidade']} e disse: "{user_input}"

# Pergunte que data ele prefere, de forma natural. Sugira que informe no formato DD/MM/AAAA."""
        
#         resposta = llm(prompt)
#         contexto["etapa"] = "coeltando_data"
#         return resposta, contexto
#     else:

#         if dados.get("confirmado"):
#             resultado_tool = consultas_tool(
#                 acao="agendar",
#                 paciente_id=1,
#                 especialidade=dados["tipo_enxame"],
#                 data=dados["data"],
                                       
#                 )

#                 contexto["etapa"] = "concluido"
#                 contexto["dados"] = {}
#                 return resultado_tool, contexto
#         else:
#             from datetime import datetime
#             data_formada = datetime.strptime(dados["data"], "%Y-%m-%d").strftime("%d/%m/%Y")

#             confirmacao = f"""Vou confirmar os dados:
#             🩺 **Resumo do exame:**
#             • Tipo: {dados['tipo_exame'].title()}
#             • Data: {data_formatada}
#             Posso confirmar? (Digite "sim")"""

#                 contexto["etapa"] = "confirmando"
#                 return confirmacao, contexto


# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# import httpx
# import os
# from dotenv import load_dotenv
# from app.chatbot.agent_llama.tools_llama import resposta_chatbot

# load_dotenv()
# # conectar com o banco para puxar os dados
# router = APIRouter()
# NEST_BASE_URL = os.getenv("NEST_BASE_URL", "http://127.0.0.1:3000")

# class Message(BaseModel):
#     message: str 
#     id: str |  None = None

# @router.post("/fas_agent_llama")
# async def chat_endpoint(data: Message):
#     msg = data.message.strip()
#     id = data.user.id

#     try:
#         if msg == "1":
#             async with httpx.AsyncClient() as client:
#                 especialidades_resp = await client.get(
#                     f"{NEST_BASE_URL} /api/data/especilidades"
#                 )
#                 unidades_resp = await client.get(
#                     f"{NEST_BASE_URL}/api/data/unidades",
                    
#                 )
#                 convenios_resp = await client.get(
#                     f"{NEST_BASE_URL}/api/data/convenios",
                    
#                 )

#                 if especialidades_resp.status_code == 200 and unidades_resp.status_code == 200:
#                     especialidades = especialidades_resp()
#                     unidades = unidades_resp()

#                     prompt = f"""Você é um assistente de clínica médica.
#                     Especialidades disponíveis:
#                     {chr(10).join([f"- {e['nome']}: {e['descricao']}" for e in especialidades])}
#                     Unidades Disponíves:
#                     {chr(10).join([f"-{u['nome']}" for u in unidades])}
#                     Ajude o paciente a aagendar um consulta. Liste as especialidades de forma clara
#                     e pergunte qual especialidade ele deseja, em qual unidade prefere ser atendido.
#                     Seja obejtivo e amigável"""

#                     resposta = resposta_chatbot(prompt)
#                     return {"reply": resposta}
#                 else:
#                     return {"reply": resposta}
#         elif msg == "2":
#             async with httpx.AsyncClient() as client:
#                 exames_resp = await client.get(
#                     f"{NEST_BASE_URL}/api/data/tipos-enxames",
                    
#                 )
#                 unidades_resp = await client.get(
#                     f"{NEST_BASE_URL}/api/unidades",
#                 )
#                 if exames_resp.status_code == 200 and unidades_resp.status_code == 200:
#                     exames = exames_resp.json()
#                     unidades = unidades_resp.json()

#                     categorias = {}
#                     for exame in exames:
#                         cat = exame.get('categoria', 'Outros')
#                         if cat not in categorias:
#                             categorias[cat] = []
#                         categorias[cat].append(exame['nome'])
#                     exames_formatados = "\n".join([
#                         f"{cat}: {', '.join(nomes)}" for cat, nomes in categorias.items()
#                     ])
#             prompt = f"""Você é um assistente de clínica médica.

# Exames disponíveis por categoria:
# {exames_formatados}

# Unidades disponíveis:
# {chr(10).join([f"- {u['nome']}" for u in unidades])}



# Ajude o paciente a solicitar exames. Explique de forma clara os tipos de exames disponíveis
# e pergunte qual exame ele precisa fazer, em qual unidade e qual convênio possui.
# Seja objetivo e amigável."""
#     except httpx.RequestError as e:
#         print(f"Erro de conexão com backend: {e}")
#         return {"reply": "Erro ao conectar com o servidor"}            
                
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

    