# from transformers import Tool
# from sqlalchemy import text
# from database import engine, get_table_description


# table_description = get_table_description("")


# class SQLexecutorTool(Tool):
#     name = "sql_engine"

#     decription = f"""Executa consultas SQL na tabela 'consultas'.
#     Retorna uma representação em string do resultado.
#     Estrutura da tabela:
#     {table_description}"""

#     inputs = { "query":
#               {
#                   "type": "text",
#                   "descripton": "TIPO DE CONSULTA EM SQL"
#               }}
#     output_type = "text"

#     def consulte(self, query: str) -> str:

#         output = ""

#         with engine.connect() as con:
#           try:
#              rows = con.execute(text(query))
#              for row in rows:
#                 output += str(row)

#           except Exception as e:
#             return f"Erro ao executar consulta: {str(e)}"

# from transformers.agents import Tool
# from llama_conect_database_tools import executar_query

# class ConsultasTool(Tool):
#     name =""
#     descrption = ""
#     inputs ={"nome_paciente": {"type": "text", "description": "Nome do paciente"}}
#     output_type= "text"

#     def buscar(self, nome_paciente: str):
#         query = "COmando SQL"
#         return executar_query(query)
    

# class ExameTool(Tool):
#     name =""
#     descrption = ""
#     inputs ={"tipo_exame": {"type": "text", "description": "Tipo de enxame"}}
#     output_type= "text"

#     def buscar(self, tipo_exame: str):
#         query = "COmando SQL"
#         return executar_query(query)
    

# class AgendamentoTool(Tool):
#     name =""
#     descrption = ""
#     inputs ={"nome_paciente": {"type": "text", "description": "Nome do paciente"}}
#     output_type= "text"

#     def buscar(self, nome_paciente: str):
#         query = "COmando SQL"
#         return executar_query(query)
import sqlite3
from typing import List, Dict, Any
from datetime import datetime
import json

class DatabaseConnection:
    def __init__(self, dp_path: str =""):
        self.conn = psycopg2.connect(
            host="",
            database="",
            user="",
            password=""
        )
        self.dp_path = dp_path
        self.conn = None
    
    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None  

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:

         conn = self.connect()
         cursor = conn.cursor()
         cursor.execute(query, params)

         columns = [description[0] for description in cursor.description ]
         results = []
         for row in cursor.fetchall():
             results.append(dict(zip(columns, row)))
         return results      

    def execute_inset(self, quey: str, params: tuple  =()) -> int:

         conn = self.connect()
         cursor = conn.cursor()
         cursor.execute(quey, params)
         conn.commit()
         return cursor.lastrowid
    
db= DatabaseConnection()

        

   