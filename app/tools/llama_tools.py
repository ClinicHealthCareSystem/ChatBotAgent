from transformers import Tool
from sqlalchemy import text
from database import engine, get_table_description


table_description = get_table_description("")


class SQLexecutorTool(Tool):
    name = "sql_engine"

    decription = f"""Executa consultas SQL na tabela 'consultas'.
    Retorna uma representação em string do resultado.
    Estrutura da tabela:
    {table_description}"""

    inputs = { "query":
              {
                  "type": "text",
                  "descripton": "TIPO DE CONSULTA EM SQL"
              }}
    output_type = "text"

    def consulte(self, query: str) -> str:

        output = ""

        with engine.connect() as con:
          try:
             rows = con.execute(text(query))
             for row in rows:
                output += str(row)

          except Exception as e:
            return f"Erro ao executar consulta: {str(e)}"