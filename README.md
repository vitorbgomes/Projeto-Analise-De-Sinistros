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

🔗 [Link do Painel Interativo - https://lookerstudio.google.com/reporting/33e5333e-b193-44d2-8dd1-34bc297722e2

**Contém:**

- Visualização de Dados com os Resultados
Para que os insights sejam consumidos de forma eficaz, foi desenvolvido um dashboard no Looker Studio, dividido em três painéis estratégicos, cada um com um público-alvo específico.

- Dashboard - Visão Geral
Dashboard Visão Geral
Ideal para executivos, oferece uma visão macro da sinistralidade, com mapa de calor, principais causas e incidência por estado.

- Dashboard - Gestor de Frotas
Dashboard Gestor de Frotas
Focado em otimizar a operação, reduzir custos e garantir a segurança, analisando causas, tipos de acidente e zonas de alta incidência.

- Dashboard - Seguradoras
Dashboard Seguradoras
Ferramenta estratégica para subscritores e analistas de risco, com calculadora de risco dinâmica e mapa de calor por rodovia.
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
