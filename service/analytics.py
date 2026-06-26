# analytics.py
import pandas as pd
import matplotlib.pyplot as plt
import config
from mlxtend.frequent_patterns import apriori, association_rules

def minerar_regras(df_analise):
    print("[Analytics] Convertendo dados para formato binário (One-Hot)...")
    df_binario = pd.get_dummies(df_analise)
    
    print(f"[Analytics] Executando Apriori (Suporte Min: {config.SUPORTE_MIN})...")
    itens_frequentes = apriori(df_binario, min_support=config.SUPORTE_MIN, use_colnames=True)
    
    if itens_frequentes.empty:
        print("[Analytics] Nenhum item frequente encontrado com este suporte.")
        return None
        
    print(f"[Analytics] Gerando regras de associação (Confiança Min: {config.CONFIANCA_MIN})...")
    regras = association_rules(itens_frequentes, metric="confidence", min_threshold=config.CONFIANCA_MIN)
    
    if regras.empty:
        print("[Analytics] Nenhuma regra gerada com esta confiança.")
        return None
        
    # Formatação amigável para leitura humana
    regras['antecedents'] = regras['antecedents'].apply(lambda x: ', '.join(list(x)))
    regras['consequents'] = regras['consequents'].apply(lambda x: ', '.join(list(x)))
    
    # Ordenamos as regras pelas mais fortes (maior lift) no topo
    regras = regras.sort_values(by='lift', ascending=False)
    
    print(f"[Analytics] {len(regras)} regras criadas com sucesso.")
    return regras

def plotar_resultados(regras):
    if regras is None or regras.empty:
        return
        
    print("[Analytics] Gerando e salvando gráfico de dispersão...")
    plt.figure(figsize=(10, 6)) # Retornando ao tamanho original
    scatter = plt.scatter(
        regras['support'], regras['confidence'], 
        c=regras['lift'], cmap='viridis', alpha=0.8, s=100
    )

    plt.colorbar(scatter, label='Lift (Força da Associação)')
    plt.title('Regras Apriori: Geografia da Doença na Região Sul', fontsize=14, pad=15)
    plt.xlabel('Suporte (Frequência)', fontsize=12)
    plt.ylabel('Confiança (Precisão)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.savefig('grafico_regras_apriori.png', dpi=300, bbox_inches='tight')
    plt.show()