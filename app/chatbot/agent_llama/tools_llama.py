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
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
from app.chatbot.agent_llama.tools_llama import resposta_chatbot

load_dotenv()
# conectar com o banco para puxar os dados
router = APIRouter()
NEST_BASE_URL = os.getenv("NEST_BASE_URL", "http://127.0.0.1:3000")

class Message(BaseModel):
    message: str 
    id: str |  None = None

@router.post("/fas_agent_llama")
async def chat_endpoint(data: Message):
    msg = data.message.strip()
    id = data.user.id

    try:
        if msg == "1":
            async with httpx.AsyncClient() as client:
                especiallidades_respt = await client.get(
                    f"{NEST_BASE_URL} /api/data/especilidades"
                )
                unidades_resp = await client.get(
                    f"{NEST_BASE_URL}/api/data/unidades",
                    
                )
                 convenios_resp = await client.get(
                    f"{NEST_BASE_URL}/api/data/convenios",
                    
                )
                


    