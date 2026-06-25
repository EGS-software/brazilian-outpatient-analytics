from service import extract, transform, analytics

def main():
    print("\n" + "="*50)
    print("🏁 INICIANDO PIPELINE UNIFICADO: SIASUS REGIONAL APRIORI")
    print("="*50 + "\n")
    
    # 1. EXTRAÇÃO (Extract)
    dimensoes = extract.carregar_dimensoes()
    df_bruto_sul = extract.extrair_fatos_regiao_sul()
    
    # 2. TRANSFORMAÇÃO (Transform)
    df_fatos_pronto, dimensoes_prontas = transform.preparar_chaves(df_bruto_sul, dimensoes)
    df_enriquecido = transform.enriquecer_e_limpar(df_fatos_pronto, dimensoes_prontas)
    
    # Seleção de colunas estratégicas para o Apriori
    colunas_finais = ['ESTADO', 'DIAGNOSTICO', 'FAIXA_ETARIA', 'SEXO', 'CARATER_ATENDIMENTO']
    df_final_processado = df_enriquecido[colunas_finais].dropna()
    
    # Salva um backup físico da base limpa
    df_final_processado.to_csv('base_siasus_sul_limpa.csv', index=False)
    
    # 3. MINERAÇÃO E ANÁLISE (Analytics)
    regras_geradas = analytics.minerar_regras(df_final_processado)
    
    # 4. EXIBIÇÃO E SAÍDA
    print("\n" + "="*50)
    if regras_geradas is not None and not regras_geradas.empty:
        print("🏆 TOP 10 REGRAS ENCONTRADAS (Ordenadas por LIFT):")
        print("-" * 50)
        print(regras_geradas[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10).to_string())
        print("-" * 50)
        
        # Gera o gráfico automático
        analytics.plotar_resultados(regras_geradas)
        print("💾 Pipeline concluído! Imagem 'grafico_regras_apriori.png' gerada.")
    else:
        print("❌ Nenhuma regra forte foi encontrada com os parâmetros atuais.")
        print("💡 Dica: Abra o 'config.py' e diminua os valores de SUPORTE_MIN ou CONFIANCA_MIN.")
    print("="*50 + "\n")

if __name__ == '__main__':
    main()