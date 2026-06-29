# 🏥 Pipeline de Mineração de Dados SIASUS - Região Sul (RS)

## 📋 Visão Geral

Este projeto é um pipeline completo de **ETL (Extração, Transformação e Carga)** acoplado a um motor de **Mineração de Dados**. Ele processa arquivos de Produção Ambulatorial do SUS (SIASUS) focados na Região Sul do Brasil (especificamente Rio Grande do Sul), com o objetivo de descobrir padrões ocultos na saúde pública utilizando o algoritmo **Apriori** (Regras de Associação).

O sistema cruza dados geográficos (Municípios), demográficos (Idade, Sexo) e clínicos (CID, Caráter de Atendimento) para entender a "Geografia da Doença", identificando quais perfis de pacientes e diagnósticos estão mais associados a determinadas localidades.

---

## ⚙️ Arquitetura e Módulos

O projeto está dividido de forma modular, separando responsabilidades:

* **`main.py`**: O orquestrador central. Gerencia o fluxo de execução desde a leitura bruta até a geração do gráfico final.
* **`extract.py`**: Responsável pela ingestão de dados. Possui leitura otimizada em *chunks* e gerenciamento ativo de memória (`gc.collect()`) para lidar com bases de dados massivas do DataSUS.
* **`transform.py`**: Responsável pela higienização e enriquecimento. Realiza os *merges* com tabelas de domínio (Municípios, CIDs, CBOs), discretiza idades (Criança, Jovem, Adulto, Idoso) e limpa registros inconsistentes.
* **`analytics.py`**: O motor analítico. Transforma os dados limpos em formato binário (One-Hot), aplica o algoritmo Apriori para gerar itens frequentes e extrai regras de associação baseadas em Confiança e *Lift*. Também gera a visualização gráfica dos resultados.

---

## 🧠 Variáveis Analisadas

O modelo Apriori busca associações entre as seguintes variáveis categóricas:

* 📍 **Município de Atendimento**
* 🩺 **Diagnóstico (CID - Título)**
* 👥 **Faixa Etária** (Criança, Jovem, Adulto, Idoso)
* 🚻 **Sexo** (Masculino, Feminino)
* 🚑 **Caráter do Atendimento** (Urgência, Eletivo)

---

## 🚀 Como Executar

### Pré-requisitos

Certifique-se de ter o Python 3.8+ instalado e instale as dependências executando:

```bash
pip install pandas matplotlib mlxtend

```

### Configuração

O projeto depende de um arquivo `config.py` (não incluído neste repositório) que deve conter as seguintes variáveis:

* `BASE_PATH`: Caminho do diretório onde estão os arquivos `.csv` do DataSUS.
* `ARQUIVOS_PRODUCAO`: Lista com os nomes dos arquivos de fatos do SIASUS (ex: `['PABA2301.csv', ...]`).
* `CHUNK_SIZE`: Tamanho do lote para leitura (ex: `100000`).
* `SUPORTE_MIN`: Limite mínimo de suporte para o Apriori (ex: `0.01`).
* `CONFIANCA_MIN`: Limite mínimo de confiança para as regras (ex: `0.5`).

### Execução

Para rodar o pipeline completo, execute:

```bash
python main.py

```

---

## 📊 Resultados e Saídas

Após a execução bem-sucedida, o pipeline gera automaticamente dois artefatos na raiz do projeto:

1. **`base_siasus_municipios_rs_limpa.csv`**: Um backup físico dos dados já higienizados, cruzados e discretizados, pronto para ser consumido por ferramentas de BI (como PowerBI ou Metabase).
2. **`grafico_regras_apriori.png`**: Um gráfico de dispersão (Scatter Plot) ilustrando as regras encontradas, onde os eixos representam Suporte e Confiança, e a cor mapeia a força da regra (*Lift*). No terminal, as **Top 10 Regras** mais fortes também serão impressas.

---

## 🛠️ Notas de Desempenho

Devido ao volume massivo dos arquivos do DataSUS, este projeto foi desenhado com foco em eficiência de memória RAM. O uso do parâmetro `chunksize` no Pandas e a invocação manual do *Garbage Collector* (`gc`) garantem que o sistema não sofra travamentos (Out of Memory) durante a etapa de extração.

---

## 🤝 Contribuidores

* [@jvbenetti](https://github.com/jvbenetti)
* [@Txagouuu](https://github.com/Txagouuu)