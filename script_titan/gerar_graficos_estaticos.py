import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# 1. Configuração de Ambiente
base_path = os.path.dirname(__file__)
dotenv_path = os.path.join(base_path, '..', '.env')
load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# 2. Busca os dados (últimas 24 horas ou os últimos 100 registros)
query = "SELECT * FROM dados_tempo_real ORDER BY timestamp ASC LIMIT 100"
df = pd.read_sql(query, engine)

# Converte o timestamp para o formato de data do Python
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 3. Configuração do Layout Moderno (Dark Mode & Neon)
plt.style.use('dark_background')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 14), facecolor='#121212')
plt.subplots_adjust(hspace=0.5) # Espaço entre os gráficos

# Paleta de Cores Tecnológica
color_rpm = '#00E5FF'      # Ciano neon
color_vib = '#FF2A6D'      # Rosa neon
color_health = '#05FFA1'   # Verde neon
bg_axes = '#1E1E24'        # Fundo dos gráficos
grid_color = '#383842'     # Cor da grade

# Aplica estilização base para todos os eixos
for ax in [ax1, ax2, ax3]:
    ax.set_facecolor(bg_axes)
    ax.grid(True, color=grid_color, linestyle='--', linewidth=0.7, alpha=0.8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#555566')
    ax.spines['bottom'].set_color('#555566')
    ax.tick_params(colors='#B0B0C0')

# --- GRÁFICO 1: RPM ---
ax1.plot(df['timestamp'], df['rpm'], color=color_rpm, linewidth=2.5)
ax1.fill_between(df['timestamp'], df['rpm'], color=color_rpm, alpha=0.1) # Efeito de brilho
ax1.set_title('Monitoramento de Rotações (RPM)', fontsize=15, fontweight='bold', color='white', pad=15)
ax1.set_ylabel('RPM', color='#CCCCCC', fontsize=11)

# --- GRÁFICO 2: VIBRAÇÃO ---
ax2.plot(df['timestamp'], df['vibracao'], color=color_vib, linewidth=2.5)
ax2.fill_between(df['timestamp'], df['vibracao'], color=color_vib, alpha=0.1)
ax2.axhline(y=0.8, color='#FFD700', linestyle='-.', linewidth=2, label='Limite de Alerta') # Linha de alerta
ax2.set_title('Níveis de Vibração Transversal', fontsize=15, fontweight='bold', color='white', pad=15)
ax2.set_ylabel('Vibração (mm/s)', color='#CCCCCC', fontsize=11)
ax2.legend(facecolor=bg_axes, edgecolor='#555566', labelcolor='white')

# --- GRÁFICO 3: SAÚDE (Área) ---
health_pct = df['health'] * 100
ax3.plot(df['timestamp'], health_pct, color=color_health, linewidth=2.5)
ax3.fill_between(df['timestamp'], health_pct, color=color_health, alpha=0.2)
ax3.set_title('Índice de Saúde da Máquina (%)', fontsize=15, fontweight='bold', color='white', pad=15)
ax3.set_ylabel('Saúde %', color='#CCCCCC', fontsize=11)
ax3.set_ylim(0, 110)

# 4. Finalização e Salvamento
print("📊 Gerando gráficos modernos do TitanMotors...")
plt.xlabel('Tempo', color='#CCCCCC', fontsize=12)
fig.autofmt_xdate() # Formata as datas no eixo X para melhor leitura
plt.savefig('analise_estatica_titan.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
print("✅ Sucesso! O arquivo 'analise_estatica_titan.png' foi criado na pasta com o novo visual.")
plt.show()