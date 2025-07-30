# 🚗 Projeto de Análise de Sinistros Automotivos – PRF Brasil

Este projeto realiza uma análise completa de acidentes registrados pela Polícia Rodoviária Federal (PRF), com foco em prever a **gravidade dos sinistros** utilizando **Machine Learning**, e transformar esses dados em **insights visuais no Looker Studio**.

---

## 🧠 Objetivo

Criar uma estratégia de dados para o setor privado (seguradoras, transportadoras, órgãos de segurança) com base em:

- Dados públicos de sinistros rodoviários.
- Técnicas de EDA (Análise Exploratória de Dados).
- Algoritmos de aprendizado supervisionado (Random Forest).
- Visualização e interpretação dos resultados via BI.

---

## 📂 Estrutura do Projeto

📁 /projeto-sinistros/
├── 📄 relatorio_final.md # Documento dissertativo com problema, justificativa e insights
├── 🧠 script_analise_completa.py # Script Python com EDA, ML e exportação
├── 📊 importancia_variaveis_modelo.csv # Tabela com ranking das variáveis mais importantes
├── 📈 importancia_variaveis.png # Gráfico de importância gerado pelo modelo
├── 📁 dados/
│ ├── acidentes_2023.zip # Arquivo baixado da PRF (via gdown)
│ └── dados_sinistros_para_looker.xlsx # Planilha final pronta para BI
├── 📸 dashboard_looker_studio.png # Print ilustrativo do dashboard (BI)


---

## 📥 Fonte dos Dados

- Dados públicos da PRF (Polícia Rodoviária Federal)
- Link original: https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos

---

## 🔍 Etapas do Projeto

### 1. Coleta e Pré-processamento
- Download direto via Google Drive (`gdown`)
- Extração do `.csv` contido no `.zip`
- Conversão de tipos e remoção de registros inválidos

### 2. EDA (Análise Exploratória)
- Criação de variáveis derivadas: ano, mês, hora, gravidade binária
- Análises descritivas: horário de maior ocorrência, tipos de acidentes, BRs mais perigosas
- Gravação de insights em relatório técnico

### 3. Modelo de Machine Learning
- Algoritmo: `RandomForestClassifier`
- Pipeline de pré-processamento com `OneHotEncoder`
- Avaliação com `classification_report`
- Previsão de gravidade e probabilidade de risco

### 4. Explicabilidade do Modelo
- Geração automática de:
  - `importancia_variaveis_modelo.csv`
  - `importancia_variaveis.png`

### 5. Exportação e Visualização
- Exportação da base preditiva para `.xlsx` ou `.csv`
- Conexão ao Looker Studio para construção de dashboards

---

## 📊 Dashboard Looker Studio

🔗 [Link do Painel Interativo - Exemplo](https://lookerstudio.google.com) *(substituir pelo seu link)*

**Contém:**

- Mapa com hotspots de acidentes
- Gráfico por tipo de acidente e probabilidade de gravidade
- Filtros por estado, BR, horário, condição climática
- Interpretação com base na previsão do modelo

---

## 📌 Principais Insights

- O modelo alcançou **90% de acurácia**, com destaque para precisão em prever casos não graves.
- A maioria dos acidentes graves acontece em **pista simples, sob chuva e em colisões frontais**.
- A previsão de risco permite **ranquear BRs e municípios mais críticos**.
- **Semana e hora do dia** influenciam diretamente na gravidade esperada.

---

## 🚀 Como Reproduzir

### Requisitos

- Python 3.9+
- Pandas, Scikit-learn, Matplotlib, gdown, openpyxl

### Execução

```bash
pip install -r requirements.txt
python script_analise_completa.py
