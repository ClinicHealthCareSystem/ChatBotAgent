import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import json
import re
from typing import Dict, Any, Optional

load_dotenv()
token = os.getenv("HF_API_TOKEN")

client = InferenceClient(model="meta-llama/Llama-3.1-8B-Instruct", token=token)


PACIENTE_ID = 1

SYSTEM_PROMPT = """
Você é um assisten virtual de uma clínica médica chamda Sáude Mania.
Seu objetivo é ajudar pacientes de forma educada, clara e profissional em portugês do Brasil.

Faça perguntas claras e objetivas.
"""

def detectar_opcao_menu(texto: str) -> Optional[int]:
    texto = texto.strip()

    if texto in ["1", "2", "3", "4"]:
        return int(texto)

    texto_lower = texto.lower()
    if any(palavra in texto_lower for palavra in ["consulta", "agendar consulta","marcar consulta"]):
        return 1
    elif any(palavra in texto_lower for palavra in ["enxame", "agendar enxame","marcar enxame"]):
        return 2
    elif any(palavra in texto_lower for palavra in ["agendamento", "ver agendamentos","meus agendamentos"]):
        return 3
    elif any(palavra in texto_lower for palavra in ["dúvidas", "ajuda"]):
        return 4
    
    return None
    
def dados_consuta(texto: str) -> Dict:
    dados = {}

    especialidade ={
        "clínico geral": ["clínico", "clinico", "geral", "clínica geral"],
        "pediatria": ["pediatr", "criança", "crianca", "infantil"],
        "geriatria": ["geriatra", "geriatri", "velho", "idoso","geriatr"]
    }
    texto_lower = texto.lower()
    for espec, palavras in especialidade.items():
        if any(p in texto_lower for p in palavras):
            dados["especialidades"] = espec
            break
    
    match_data = re.search(r'(\d{1,2})[/-](\d{1,2})(?:[/-](\d{4}))?', texto)
    if match_data:
        dia, mes, ano = match_data.groups()
        ano = ano or "2025"
        dados["data"] = f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"

    match_hora = re.search(r'(\d{1,2})[h:](\d{2})?', texto)
    if match_hora:
        hora = match_hora.group(1).zfill(2)
        minuto = match_hora.group(2) or "00"
        dados["hora"] = f"{hora}:{minuto}"
    
    if any(palavra in texto_lower for palavra in ["sim",  "confirmar", "ok", "correto", "isso", "confirmo"]):
        dados["confirmado"] = True

    return dados

def dados_exames(texto: str) -> Dict:
    dados = {}

    tipos_enxames ={
        "hemograma completo": ["hemograma","enxame de sangue", "sangue completo"],
        "raio x": ["raio-x", "raio x", "rx"],
    }

    texto_lower = texto.lower()
    for espec, palavras in tipos_enxames.items():
        if any(p in texto_lower for p in palavras):
            dados["tipos_enxames"] = espec
            break

    match_data = re.search(r'(\d{1,2})[/-](\d{1,2})(?:[/-](\d{4}))?', texto)
    if match_data:
        dia, mes, ano = match_data.groups()
        ano = ano or "2025"
        dados["data"] = f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"

    match_hora = re.search(r'(\d{1,2})[h:](\d{2})?', texto)
    if match_hora:
        hora = match_hora.group(1).zfill(2)
        minuto = match_hora.group(2) or "80"
        dados["hora"] = f"{hora}:{minuto}"
    
    if any(palavra in texto_lower for palavra in ["sim",  "confirmar", "ok", "correto", "isso", "confirmo"]):
        dados["confirmado"] = True

    return dados

def llm(prompt: str) -> str:
    
        resposta = client.chat.completions.create(
            messages=[
                 {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        return resposta.choices[0].message.content.strip()
    