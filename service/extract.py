import pandas as pd
import os
import config
import gc  # Biblioteca para forçar a limpeza da memória RAM (Garbage Collector)

def carregar_dimensoes():
    print("[Extract] Carregando tabelas de dimensão (versão otimizada em RAM)...")
    # Usamos o 'usecols' para carregar APENAS as colunas que importam de cada dicionário.
    dimensoes = {
        'procedimentos': pd.read_csv(os.path.join(config.BASE_PATH, 'TB_SIGTAW.csv'), encoding='latin1', usecols=['IP_COD', 'IP_DSCR'], dtype=str),
        'municipios': pd.read_csv(os.path.join(config.BASE_PATH, 'tb_municip.csv'), encoding='latin1', usecols=['CO_MUNICIP', 'DS_NOME', 'CO_UF'], dtype=str),
        'cid': pd.read_csv(os.path.join(config.BASE_PATH, 'S_CID.csv'), encoding='latin1', usecols=['CD_COD', 'CD_DESCR'], dtype=str),
        'cbo': pd.read_csv(os.path.join(config.BASE_PATH, 'CBO.csv'), encoding='latin1', usecols=['CBO', 'DS_CBO'], dtype=str)
    }
    print("[Extract] Dicionários carregados com sucesso (memória reduzida).")
    return dimensoes

def extrair_fatos_regiao_sul():
    lista_chunks_sul = []
    print("[Extract] Iniciando leitura otimizada (Foco na Região Sul + Seleção de Colunas)...")
    
    colunas_uteis = [
        'PA_UFMUN', 'PA_MUNPCN', 'PA_PROC_ID', 
        'PA_CIDPRI', 'PA_CBOCOD', 'PA_SEXO', 
        'PA_INCURG', 'PA_IDADE'
    ]
    
    for arquivo in config.ARQUIVOS_PRODUCAO:
        caminho_completo = os.path.join(config.BASE_PATH, arquivo)
        print(f"Lendo arquivo: {caminho_completo}")
        
        # Adicionamos dtype=str para forçar tudo a ser texto e evitar bugs do Pandas
        with pd.read_csv(caminho_completo, encoding='latin1', usecols=colunas_uteis, chunksize=config.CHUNK_SIZE, dtype=str) as reader:
            for chunk in reader:
                chunk['PA_UFMUN'] = chunk['PA_UFMUN'].astype(str)
                chunk_filtrado = chunk[chunk['PA_UFMUN'].str.startswith('4')]
                
                if not chunk_filtrado.empty:
                    lista_chunks_sul.append(chunk_filtrado)
            
            # Força o sistema a liberar a memória lixo acumulada após cada arquivo grande
            gc.collect()
                    
    print("[Extract] Concatenando os dados filtrados...")
    df_fatos_sul = pd.concat(lista_chunks_sul, ignore_index=True)
    
    # Destrói a lista de pedaços original da memória
    del lista_chunks_sul
    gc.collect()
    
    print(f"[Extract] Extração concluída. Total bruto da Região Sul: {len(df_fatos_sul)}")
    return df_fatos_sul