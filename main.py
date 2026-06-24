# main.py
from service import extract, transform

def main():
    print("\n" + "="*45)
    print("🏁 INICIANDO PIPELINE: GEOGRAFIA DA DOENÇA SUL")
    print("="*45 + "\n")
    
    # 1. EXTRAÇÃO
    dimensoes = extract.carregar_dimensoes()
    df_bruto_sul = extract.extrair_fatos_regiao_sul()
    
    # 2. TRANSFORMAÇÃO
    df_fatos_pronto, dimensoes_prontas = transform.preparar_chaves(df_bruto_sul, dimensoes)
    df_enriquecido = transform.enriquecer_e_limpar(df_fatos_pronto, dimensoes_prontas)
    
    # 3. SELEÇÃO DE COLUNAS PARA O APRIORI (O recorte perfeito para o trabalho)
    colunas_apriori = ['ESTADO', 'DIAGNOSTICO', 'FAIXA_ETARIA', 'SEXO', 'CARATER_ATENDIMENTO']
    df_final_apriori = df_enriquecido[colunas_apriori].dropna()
    
    # 4. SALVAMENTO (LOAD)
    arquivo_saida = 'base_siasus_sul_para_apriori.csv'
    df_final_apriori.to_csv(arquivo_saida, index=False)
    
    print("\n" + "="*45)
    print("🎉 PIPELINE EXECUTADO COM SUCESSO!")
    print(f"💾 Base pronta salva em: {arquivo_saida}")
    print(f"📊 Quantidade de registros prontos: {len(df_final_apriori)}")
    print("="*45 + "\n")
    
    # Exibe uma prévia de como os dados ficaram para o seu colega rodar o Apriori
    print("👀 Prévia dos dados estruturados:")
    print(df_final_apriori.head())

if __name__ == '__main__':
    main()