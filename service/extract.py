# extract.py
import pandas as pd
import config

def carregar_dimensoes():
    """Carrega as tabelas de dicionários/dimensões."""
    print("📦 [Extract] Carregando tabelas de dimensão...")
    dimensoes = {
        'procedimentos': pd.read_csv(config.BASE_PATH + 'TB_SIGTAW.csv', encoding='latin1', low_memory=False),
        'municipios': pd.read_csv(config.BASE_PATH + 'tb_municip.csv', encoding='latin1', low_memory=False),
        'cid': pd.read_csv(config.BASE_PATH + 'S_CID.csv', encoding='latin1', low_memory=False),
        'cbo': pd.read_csv(config.BASE_PATH + 'CBO.csv', encoding='latin1', low_memory=False)
    }
    print("✔️ [Extract] Dicionários carregados com sucesso.")
    return dimensoes

def extrair_fatos_regiao_sul():
    """Lê as tabelas fato em chunks e filtra apenas a Região Sul."""
    lista_chunks_sul = []
    print("🚀 [Extract] Iniciando leitura otimizada (Foco na Região Sul)...")
    
    for arquivo in config.ARQUIVOS_PRODUCAO:
        caminho_completo = config.BASE_PATH + arquivo
        print(f"📖 Lendo arquivo: {caminho_completo}")
        
        with pd.read_csv(caminho_completo, encoding='latin1', low_memory=False, chunksize=config.CHUNK_SIZE) as reader:
            for chunk in reader:
                # Garante que o código do município é string para filtrar pelo primeiro dígito
                chunk['PA_UFMUN'] = chunk['PA_UFMUN'].astype(str)
                
                # O dígito '4' representa o início dos códigos do IBGE da Região Sul (PR, SC, RS)
                chunk_filtrado = chunk[chunk['PA_UFMUN'].str.startswith('4')]
                
                if not chunk_filtrado.empty:
                    lista_chunks_sul.append(chunk_filtrado)
                    
    df_fatos_sul = pd.concat(lista_chunks_sul, ignore_index=True)
    print(f"✔️ [Extract] Extração concluída. Total de registros da Região Sul: {len(df_fatos_sul)}")
    return df_fatos_sul