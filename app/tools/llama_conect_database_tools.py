# from sqlalchemy import create_engine, text
# import os
# from dotenv import load_dotenv

# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")

# engine= create_engine(DATABASE_URL)

# def executar_query(query):
#     try:
#         result = connection.execute(text(query))
#         linhas = result.fetchall()
#         return linhas
#     except Exception as e:
#         return f"ERRO ao consultar{e}"