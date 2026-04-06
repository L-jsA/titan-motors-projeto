from fastapi import FastAPI
from sqlalchemy import create_engine, text
import pandas as pd
import os # <-- Faltava importar este
from dotenv import load_dotenv # <-- Faltava importar este
from fastapi.middleware.cors import CORSMiddleware

# Carrega as configurações do arquivo .env que está na pasta de cima
base_path = os.path.dirname(__file__)
dotenv_path = os.path.join(base_path, '..', '.env')
load_dotenv(dotenv_path)

app = FastAPI()

# Permite que seu front-end acesse a API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agora o os.getenv vai conseguir buscar a URL que você colou no .env
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Ajuste de caminho para o CSV (caso ainda queira usar como fallback)
caminho_csv = os.path.join(base_path, '..', 'dataset_tratado.csv')

@app.get("/dados")
def get_dados():
    query = "SELECT * FROM dados_tempo_real ORDER BY ctid DESC LIMIT 50"
    
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"erro": f"Falha ao conectar ao banco: {e}"}

@app.get("/status")
def get_status():
    return {"status": "Online", "database": "Conectado ao Neon"}