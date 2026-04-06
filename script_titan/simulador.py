import pandas as pd
import time
import os
import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1. Configurações de Caminho e Ambiente
base_path = os.path.dirname(__file__)
# Sobe um nível para achar o .env e o dataset na raiz do projeto
dotenv_path = os.path.join(base_path, '..', '.env')
load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("ERRO: DATABASE_URL não encontrada no .env!")

# 2. Conexão com o Banco e Carga de Dados
engine = create_engine(DATABASE_URL)
caminho_csv = os.path.join(base_path, '..', 'dataset_tratado.csv')

# ESTA LINHA DEFINE O 'df' - Ela precisa vir antes do loop!
df = pd.read_csv(caminho_csv)

print("🚀 Simulador TitanMotors iniciado...")

# 3. Loop de Simulação
while True:
    for i, row in df.iterrows():
        linha = row.to_frame().T
        
        # ATUALIZAÇÃO CRÍTICA: Gera o horário de agora para o banco
        linha['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            # Envia para o Neon
            linha.to_sql('dados_tempo_real', engine, if_exists='append', index=False)
            
            horario_log = linha['timestamp'].iloc[0]
            print(f"✅ Enviado: {horario_log} | RPM: {row['rpm']}")
        except Exception as e:
            print(f"❌ Erro ao salvar no Neon: {e}")
        
        # Define o intervalo de 5 minutos (300 segundos)
        time.sleep(300)