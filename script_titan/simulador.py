import pandas as pd
import time
import os
import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

# 1. Configuração de Caminhos e Ambiente
base_path = Path(__file__).resolve().parent
env_path = base_path.parent / '.env'
load_dotenv(dotenv_path=env_path)

caminho_csv = base_path.parent / 'dataset_tratado.csv'

# 2. Verificação do CSV e Variáveis
if not os.path.exists(caminho_csv):
    raise FileNotFoundError(f"❌ Erro: Arquivo {caminho_csv} não encontrado!")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ ERRO: DATABASE_URL não encontrada no .env!")

# 3. Configuração da Conexão (Versão Anti-Oscilação de Rede)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "sslmode": "require",
        "connect_timeout": 60,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5
    }
)

# 4. Carga Inicial
df = pd.read_csv(caminho_csv)
print(f"✅ CSV carregado com sucesso de: {caminho_csv}")
print("🚀 Simulador TitanMotors iniciado...")

# 5. Loop de Simulação com Sistema de Re-tentativa
while True:
    for i, row in df.iterrows():
        # Prepara a linha para o banco
        linha = row.to_frame().T
        agora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        linha['timestamp'] = agora
        
        sucesso = False
        while not sucesso:
            try:
                # Tenta enviar para o Neon
                linha.to_sql('dados_tempo_real', engine, if_exists='append', index=False)
                print(f"✅ Enviado com sucesso: {agora} | RPM: {row['rpm']}")
                sucesso = True # Sai do loop de tentativa
            except Exception as e:
                print(f"⚠️ A rede oscilou (Ping alto detectado). Tentando novamente em 10 segundos...")
                # Opcional: print(f"Erro técnico: {e}") 
                time.sleep(10) # Espera a internet estabilizar
        
        # Intervalo entre as leituras dos sensores (5 minutos conforme seu projeto)
        print(f"⏳ Aguardando 5 minutos para a próxima leitura...")
        time.sleep(300)