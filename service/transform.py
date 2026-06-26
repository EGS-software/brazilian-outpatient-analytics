import config
import pandas as pd

def preparar_chaves(df_fatos, dimensoes):
    """Padroniza os tipos de dados das colunas-chave."""
    print("[Transform] Padronizando tipos de dados das chaves...")
    
    # Chaves dos Fatos
    df_fatos['PA_MUNPCN'] = df_fatos['PA_MUNPCN'].astype(str)
    df_fatos['PA_PROC_ID'] = df_fatos['PA_PROC_ID'].astype(str)
    df_fatos['PA_CIDPRI'] = df_fatos['PA_CIDPRI'].astype(str)
    df_fatos['PA_CBOCOD'] = df_fatos['PA_CBOCOD'].astype(str)
    
    # Chaves das Dimensões
    dimensoes['municipios']['CO_MUNICIP'] = dimensoes['municipios']['CO_MUNICIP'].astype(str)
    dimensoes['procedimentos']['IP_COD'] = dimensoes['procedimentos']['IP_COD'].astype(str)
    dimensoes['cid']['CD_COD'] = dimensoes['cid']['CD_COD'].astype(str)
    dimensoes['cbo']['CBO'] = dimensoes['cbo']['CBO'].astype(str)
    
    return df_fatos, dimensoes

def discretizar_idade(idade):
    """Transforma a idade numérica em categorias de faixas etárias para o Apriori."""
    try:
        id_int = int(idade)
        if id_int <= 12: return 'Idade: Crianca'
        elif id_int <= 19: return 'Idade: Jovem'
        elif id_int <= 59: return 'Idade: Adulto'
        else: return 'Idade: Idoso'
    except:
        return 'Idade: Nao Informada'

def enriquecer_e_limpar(df_fatos, dimensoes):
    """Cruza os dados, cria variáveis geográficas e limpa inconsistências."""
    print("[Transform] Iniciando cruzamento de dados (Merges)...")
    
    # 1. Cria a coluna do Estado baseado nos 2 primeiros dígitos do município do atendimento (PA_UFMUN)
    df_fatos['COD_UF'] = df_fatos['PA_UFMUN'].str[:2]
    df_fatos['ESTADO'] = df_fatos['COD_UF'].map(config.MAPEAMENTO_ESTADOS)
    
    # 2. Merge com as colunas de tradução das dimensões
    df_analise = pd.merge(
        df_fatos, dimensoes['cid'][['CD_COD', 'CD_DESCR']], 
        left_on='PA_CIDPRI', right_on='CD_COD', how='left'
    ).rename(columns={'CD_DESCR': 'DIAGNOSTICO'})
    
    df_analise = pd.merge(
        df_analise, dimensoes['cbo'][['CBO', 'DS_CBO']], 
        left_on='PA_CBOCOD', right_on='CBO', how='left'
    ).rename(columns={'DS_CBO': 'OCUPACAO_MEDICO'})

    # 3. Limpeza de Dados
    print("[Transform] Aplicando filtros de limpeza de dados...")
    # Remove diagnósticos nulos ou não informados comumente no SIASUS
    df_analise = df_analise[
        df_analise['DIAGNOSTICO'].notna() & 
        (df_analise['PA_CIDPRI'] != '0000') & 
        (~df_analise['DIAGNOSTICO'].str.contains('NÃO INFORMADO', case=False, na=False))
    ]
    
    # Mapeia o Sexo para ficar amigável
    df_analise['SEXO'] = df_analise['PA_SEXO'].map({'M': 'Sexo: Masculino', 'F': 'Sexo: Feminino'})
    
    # Mapeia o Caráter de Atendimento
    # No SIASUS: 01 é Eletivo, 02 é Urgência/Emergência. Outros códigos variam.
    df_analise['CARATER_ATENDIMENTO'] = df_analise['PA_INCURG'].apply(
        lambda x: 'Atendimento: Urgencia' if str(x).zfill(2) == '02' else 'Atendimento: Eletivo'
    )
    
    # 4. Discretização da Idade
    df_analise['FAIXA_ETARIA'] = df_analise['PA_IDADE'].apply(discretizar_idade)
    
    # Limpa descrições de CIDs para não ficarem gigantes no Apriori (Pega as primeiras palavras ou código + nome curto)
    df_analise['DIAGNOSTICO'] = 'CID: ' + df_analise['DIAGNOSTICO'].str.slice(0, 30)
    df_analise['ESTADO'] = 'Estado: ' + df_analise['ESTADO'].astype(str)
    
    print("✔️ [Transform] Base de análise geográfica higienizada.")
    return df_analise