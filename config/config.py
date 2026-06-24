"""Configurações do projeto"""
# Caminho base dos arquivos
BASE_PATH = './brazilian-outpatient-analytics/data'

# Configurações de Processamento
CHUNK_SIZE = 500000

# Arquivos Fato do SIASUS (Produção Ambulatorial)
ARQUIVOS_PRODUCAO = [
    'PARS2501.csv',
    'PARS2505.csv',
    'PARS2508.csv'
]

# Mapeamento dos códigos de UF da Região Sul para o relatório
MAPEAMENTO_ESTADOS = {
    '41': 'Parana',
    '42': 'Santa Catarina',
    '43': 'Rio Grande do Sul'
}