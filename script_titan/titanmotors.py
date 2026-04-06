import pandas as pd

# Lê o arquivo CSV original com os dados de manutenção preditiva
df = pd.read_csv('dados_titan/predictive_maintenance.csv')

# Cria uma coluna de tempo (timestamp), gerando datas sequenciais de 1 em 1 segundo
df['timestamp'] = pd.date_range(start='2026-01-01', periods=len(df), freq='S')

# Cria a coluna de vibração baseada no torque (simulação física do comportamento do equipamento)
df['vibracao'] = df['Torque [Nm]'] * 0.02

# Cria a coluna de saúde do equipamento (health)
# Quanto maior o desgaste (Tool wear), menor será a saúde
df['health'] = 1 - (df['Tool wear [min]'] / df['Tool wear [min]'].max())

# Renomeia colunas para nomes mais simples e padronizados
df.rename(columns={
    'Rotational speed [rpm]': 'rpm', # velocidade de rotação
    'Process temperature [K]': 'temperatura'  # temperatura do processo
}, inplace=True)

# Salva o novo dataset tratado com as colunas criadas
df.to_csv('dataset_tratado.csv', index=False)

print(df.head())