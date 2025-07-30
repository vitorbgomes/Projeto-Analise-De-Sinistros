# -*- coding: utf-8 -*-
"""
Projeto: Análise de Sinistros Automotivos da PRF com Machine Learning
Etapas: EDA, modelo preditivo, extração de insights e exportação para BI (Looker Studio)
"""

import pandas as pd
import zipfile
import gdown
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

def processar_dados_sinistros_para_bi(ano=2023, nome_arquivo_saida='dados_sinistros_para_looker.xlsx'):
    print(f"🔍 Iniciando o processo para o ano de {ano}...")

    # 1. COLETA E EXTRAÇÃO
    print("📥 Baixando e extraindo os dados da PRF via Google Drive...")
    file_id = '1-caam_dahYOf2eorq4mez04Om6DD5d_3'
    url = f'https://drive.google.com/uc?id={file_id}'
    zip_output = f'dados_acidentes_{ano}.zip'

    try:
        gdown.download(url, zip_output, quiet=False)
        with zipfile.ZipFile(zip_output, 'r') as zip_file:
            csv_filename = next(name for name in zip_file.namelist() if name.lower().endswith('.csv'))
            zip_file.extract(csv_filename, path='.')
    except Exception as e:
        print(f"Erro ao baixar ou extrair o arquivo: {e}")
        return

    # 2. EDA - LIMPEZA E PRÉ-PROCESSAMENTO
    print(f"📄 Arquivo {csv_filename} extraído. Carregando e limpando...")
    try:
        df = pd.read_csv(csv_filename, encoding='latin-1', sep=';')
    except Exception as e:
        print(f"Erro ao carregar o CSV: {e}")
        os.remove(csv_filename)
        return

    df['data_inversa'] = pd.to_datetime(df['data_inversa'], errors='coerce')
    for col in ['latitude', 'longitude', 'km']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

    colunas_relevantes = [
        'id', 'data_inversa', 'dia_semana', 'horario', 'uf', 'br', 'km', 'municipio',
        'causa_acidente', 'tipo_acidente', 'classificacao_acidente',
        'fase_dia', 'sentido_via', 'condicao_metereologica', 'tipo_pista',
        'tracado_via', 'latitude', 'longitude', 'pessoas', 'mortos', 'feridos_leves',
        'feridos_graves', 'ilesos', 'ignorados', 'veiculos'
    ]
    colunas_existentes = [col for col in colunas_relevantes if col in df.columns]
    df_clean = df[colunas_existentes].copy()
    df_clean.dropna(subset=['latitude', 'longitude', 'classificacao_acidente', 'data_inversa'], inplace=True)

    # 3. FEATURE ENGINEERING
    print("🧪 Criando novas features para análise no Looker Studio...")
    df_clean['ano'] = df_clean['data_inversa'].dt.year
    df_clean['mes'] = df_clean['data_inversa'].dt.month
    df_clean['hora'] = pd.to_datetime(df_clean['horario'], format='%H:%M:%S', errors='coerce').dt.hour
    df_clean['alvo_grave'] = df_clean['classificacao_acidente'].apply(
        lambda x: 1 if 'Com Vítimas Fatais' in x or 'Com Vítimas Graves' in x else 0
    )
    df_clean['nivel_gravidade'] = df_clean['alvo_grave'].map({1: 'Grave ou Fatal', 0: 'Leve ou Sem Vítimas'})

    # 4. MODELAGEM PREDITIVA
    print("🤖 Treinando o modelo de Machine Learning...")
    features = ['dia_semana', 'fase_dia', 'condicao_metereologica', 'tipo_pista', 'tracado_via', 'tipo_acidente']
    target = 'alvo_grave'
    df_model_data = df_clean[features + [target]].fillna('Desconhecido')
    X = df_model_data[features]
    y = df_model_data[target]

    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), features)]
    )

    model = Pipeline(steps=[
        ('preprocessamento', preprocessor),
        ('classificador', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    # Avaliação do modelo
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    model.fit(X_train, y_train)
    y_pred_eval = model.predict(X_test)
    print("\n📊 Relatório de Classificação (Amostra de Teste):")
    print(classification_report(y_test, y_pred_eval, target_names=['Não Grave', 'Grave']))

    # 5. IMPORTÂNCIA DAS VARIÁVEIS
    print("📈 Gerando gráfico de importância das variáveis...")
    encoder = model.named_steps['preprocessamento'].named_transformers_['cat']
    feature_names_encoded = encoder.get_feature_names_out(features)
    importances = model.named_steps['classificador'].feature_importances_
    indices = np.argsort(importances)[::-1]

    top_n = 15
    top_features = feature_names_encoded[indices][:top_n]
    top_importances = importances[indices][:top_n]

    # Gráfico
    plt.figure(figsize=(10, 6))
    plt.barh(top_features[::-1], top_importances[::-1], color='darkgreen')
    plt.xlabel("Importância")
    plt.title("Top 15 Variáveis mais Relevantes para a Gravidade dos Acidentes")
    plt.tight_layout()
    plt.savefig("importancia_variaveis.png")
    plt.show()

    # Exportar CSV com todas as importâncias
    df_importancias = pd.DataFrame({
        'variavel': feature_names_encoded[indices],
        'importancia': importances[indices]
    })
    df_importancias.to_csv('importancia_variaveis_modelo.csv', index=False, encoding='utf-8-sig')
    print("📄 Arquivo 'importancia_variaveis_modelo.csv' gerado.")

    # 6. PREVISÕES PARA O BI
    print("📤 Gerando previsões e exportando para Excel/CSV...")
    X_full = df_clean[features].fillna('Desconhecido')
    df_clean['previsao_gravidade_id'] = model.predict(X_full)
    df_clean['probabilidade_ser_grave'] = model.predict_proba(X_full)[:, 1]
    df_clean['previsao_gravidade_label'] = df_clean['previsao_gravidade_id'].map({1: 'Grave ou Fatal', 0: 'Leve ou Sem Vítimas'})

    try:
        df_clean.to_excel(nome_arquivo_saida, index=False, engine='openpyxl')
        print(f"✅ Planilha '{nome_arquivo_saida}' gerada com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar Excel: {e}")
        csv_output_name = nome_arquivo_saida.replace('.xlsx', '.csv')
        df_clean.to_csv(csv_output_name, index=False, encoding='utf-8-sig')
        print(f"⚠️ Salvo como CSV: {csv_output_name}")

    # 7. LIMPEZA FINAL
    try:
        os.remove(csv_filename)
        os.remove(zip_output)
        print("🧹 Arquivos temporários removidos.")
    except Exception as e:
        print(f"Erro ao remover arquivos temporários: {e}")

# Execução direta
if __name__ == '__main__':
    ANO_ANALISE = 2023
    processar_dados_sinistros_para_bi(ano=ANO_ANALISE)
