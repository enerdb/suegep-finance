import streamlit as st
import pandas as pd
#import numpy as np


TB_Projetos = pd.read_excel('data\TbPadronizada.xlsx', 1)
TB_Acoes = pd.read_excel('data\TbPadronizada.xlsx', 2)
TB_Participantes = pd.read_excel('data\TbPadronizada.xlsx', 3)
TB_Meta_Projeto = pd.read_excel('data\TbPadronizada.xlsx', 6)
TB_R_Capacitados = pd.read_excel('data\TbPadronizada.xlsx', 7)


for i in range(8):
    table = pd.read_excel('data\TbPadronizada.xlsx', i)
    st.write(table)

def importa_repasses():
    df = pd.read_excel('data\TbPadronizada.xlsx', 0)
    df.columns = ['id_Repasse', 'Ano_Repasse', 'Fonte', 'Eixo', 'Natureza', 'Valor_Repasse_Inicial']
    df['Ajustes_Soma'] = None
    df['Ajustes_Soma'] = df['Ajustes_Soma'].fillna(0)
    df['Valor_Repasse_Autual'] = df['Valor_Repasse_Inicial'] + df['Ajustes_Soma']
    df['SEI'] = df['SEI'].fillna('')
    return df

def importa_projetos():
    df = pd.read_excel('data\TbPadronizada.xlsx', 1)
    df = df.rename(columns={'PR_ID': 'id_Projeto', 'Projeto': 'Nome_Projeto', 'Planejado (R$)': 'Valor_Planejado_Inicial', 'RP_ID': 'id_Repasse'})
    df = df[['id_Projeto', 'id_Repasse', 'Nome_Projeto', 'Valor_Planejado_Inicial',]]
    df['Ajustes_Soma'] = None
    df['Ajustes_Soma'] = df['Ajustes_Soma'].fillna(0)
    df['Valor_Planejado_Atual'] = df['Valor_Planejado_Inicial'] + df['Ajustes_Soma']
    return df

def importa_acoes():
    df = pd.read_excel('data\TbPadronizada.xlsx', 2)
    df = df.rename(columns={'AC_ID': 'id_Ação',
                            'Ação': 'Nome_Ação',
                            'PR_ID': 'id_Projeto',
                            'Tipo_de_ação': 'Tipo_Ação',
                            'Data_Início_Ação': 'Data_Início_Real',
                            'Data_Término_Ação': 'Data_Fim_Real',
                            })

    df['Data_Início_Planejado'] = df['Data_Início_Real']
    df['Data_Fim_Planejado'] = df['Data_Fim_Real']

    date_columns = ['Data_Início_Planejado', 'Data_Fim_Planejado', 'Data_Início_Real', 'Data_Fim_Real']
    df[date_columns] = pd.to_datetime(df[date_columns])
    
    
    df['Status'] = None
    df['Histórico'] = None
    df['Histórico'] = df['Histórico'].fillna('')

    # Filtrar e retornar apenas as colunas que são usadas
    colunas_usadas = ['id_Ação', 'id_Projeto', 'Nome_Ação', 'Tipo_Ação', 
                     'Data_Início_Planejado', 'Data_Fim_Planejado', 
                     'Data_Início_Real', 'Data_Fim_Real', 'Status', 'Histórico']

    return df[colunas_usadas]

def importa_contratacoes():
    df = pd.read_excel('data\TbPadronizada.xlsx', 2)
    df = df.rename(columns={'ID_Comp': 'id_Contratação', # Substituira aqui pelo código do Almada
                            'AC_ID': 'id_Ação',
                            'CNPJ' : 'CNPJ_Contratada',
                            'Contratada': 'Nome_Contratada',
                            'Data_Assinatura_Contrato': 'Data_contrato',
                            'Data_Encerramento_Contrato': 'Data_Encerramento_Contrato',
                            'Valor_Reservado': 'Valor_Reservado',
                            'Valor_Empenhado': 'Valor_Empenhado',
                            'Valor_Liquidado': 'Valor_Liquidado',
                            })
    
    
    # Determinar o status da contratação baseado na última etapa registrada
    df['Etapa_Atual'] = None  # Inicializar a coluna para o ID da etapa atual
    def determine_etapa(row):
        if pd.notna(row['Data_Encerramento_Contrato']):
            return 'Contrato Encerrado'
        elif pd.notna(row['Data_Assinatura_Contrato']):
            return 'Execução'
        elif pd.notna(row['Data_PB/TR']):
            return 'Contratação'
        else:
            return 'Planejamento'
    df['Etapa_Atual'] = df.apply(determine_etapa, axis=1)
    
    colunas_usadas = ['id_Contratação', 'id_Ação', 'CNPJ_Contratada', 'Nome_Contratada', 'Data_Contrato', 'Data_Encerramento_Contrato', 'Valor_Reservado', 'Valor_Empenhado', 'Valor_Liquidado', 'Etapa_Atual']

    return df[colunas_usadas]
    



    # id_Contratação
    # id_Ação
    # CNPJ_Contratada
    # Nome_Contratada	Data_Contrato	Data_Encerramento_Contrato	Valor_Reservado	Valor_Empenhado	Valor_Liquidado	id_Etapa_Atual

def importa_etapas():
    df_acoes  = pd.read_excel('data\TbPadronizada.xlsx', 2)

        # Renomear colunas para facilitar o acesso
    df_acoes = df_acoes.rename(columns={
        'Data_PB/TR': 'Data_PB_TR',
        'Data_Assinatura_Contrato': 'Data_Assinatura_Contrato',
        'Data_Encerramento_Contrato': 'Data_Encerramento_Contrato'
    })

    etapas = []
    id_etapa_counter = 0

    # Definir a ordem das etapas para calcular Data_fim_etapa
    ordem_etapas = [
        'DOD', 'ETP', 'PB_TR', 'Pregão', 'Assinatura_Contrato', 'Encerramento_Contrato'
    ]

    for index, row in df_acoes.iterrows():
        id_acao = row['idAcao']

        for i, tipo_etapa_raw in enumerate(ordem_etapas):
            # Normalizar o nome da coluna de data para evitar problemas com '/'
            data_col_name = f'Data_{tipo_etapa_raw}'

            data_inicio_etapa = row[data_col_name]

            # Atribuir SEI e Responsável com base no tipo de etapa
            if tipo_etapa_raw in ['DOD', 'ETP', 'PB_TR', 'Pregão']:
                sei = row['SEI_DOD']
                responsavel = row['Responsável_DOD']
            elif tipo_etapa_raw in ['Assinatura_Contrato', 'Encerramento_Contrato']:
                sei = row['SEI_Financeiro']
                responsavel = row['Responsável_Financeiro']
            else:
                sei = None
                responsavel = None

            # Calcular Data_fim_etapa
            data_fim_etapa = None
            if i + 1 < len(ordem_etapas):
                proxima_etapa_col_name = f'Data_{ordem_etapas[i+1]}'
                data_fim_etapa = row[proxima_etapa_col_name]

            # Adicionar a etapa se houver uma data de início
            if pd.notna(data_inicio_etapa):
                id_etapa_counter += 1
                # Mapear o tipo de etapa de volta para o formato original se necessário para a saída
                tipo_etapa_display = tipo_etapa_raw.replace('_TR', '/TR')
                etapas.append({
                    'id_Etapa': id_etapa_counter,
                    'idAcao': id_acao,
                    'tipo_etapa': tipo_etapa_display,
                    'SEI': sei,
                    'Responsável': responsavel,
                    'Data_início_etapa': data_inicio_etapa,
                    'Data_fim_etapa': data_fim_etapa
                })

    df_etapas = pd.DataFrame(etapas)

    # Converter colunas de data para o tipo datetime, se ainda não estiverem
    for col in ['Data_início_etapa', 'Data_fim_etapa']:
        if col in df_etapas.columns:
            df_etapas[col] = pd.to_datetime(df_etapas[col], errors='coerce')

    return df_etapas

def importa_capacitacoes():
    df_acoes  = pd.read_excel('data\TbPadronizada.xlsx', 2)
    df = df.rename(columns={'ID_Comp': 'id_Capacitação', # Definir
                            'AC_ID': 'id_Ação',
                            'Ação': 'Nome_Capacitação',
                            'Contratada': 'Nome_Escola',
                            'Nível_Capacitação':'Nível_Capacitação',
                            'Modalidade': 'Modalidade_Capacitação',
                            'Carga_Horária': 'Caraga_Horária_Horas',
                            'Vagas_Ofertadas': 'Vagas_Ofertadas',
                            'Data_Início_Ação': 'Data_Início_Real',
                            'Data_Término_Ação': 'Data_Fim_Real',
                            })
    df['Data_Início_Planejado'] = df['Data_Início_Real']
    df['Data_Fim_Planejado'] = df['Data_Fim_Real']

    colunas_usadas = ['id_Capacitação', 'id_Ação', 'Nome_Capacitação', 'Nome_Escola',
                     'Nível_Capacitação', 'Modalidade_Capacitação', 
                     'Caraga_Horária_Horas', 'Vagas_Ofertadas', 
                     'Data_Início_Planejado', 'Data_Fim_Planejado', 
                     'Data_Início_Real', 'Data_Fim_Real']
    return df[colunas_usadas]

def importa_selecoes():
    pass

def importa_inscricoes()
    pass

def importa_participantes():
    pass

def importa_tabelas_apoio():
    pass



# Modelagem athena
# AC_ID, Ação, SEI_DOD, Responsável_DOD, Coordenação, Tipo_de_ação, Nível_Capacitação, Modalidade, Carga_Horária, Vagas_Ofertadas, SEI_Seleção, Responsável_Seleção, Data_Início_Ação, Data_Término_Ação, SEI_Financeiro, Responsável_Financeiro, CNPJ, Contratada, Data_DOD, Data_ETP, Data_PB/TR, Data_Pregão, Data_Assinatura_Contrato, Data_Encerramento_Contrato, Valor_Reservado, Valor_Empenhado, Valor_Liquidado, PR_ID, ID_Comp
#   

# Transposição Modelagem nova
# Ações: AC_ID, PR_ID, Ação, Tipo_de_ação, Data_Início_Ação, Data_Término_Ação
# Contratações: CNPJ, Contratada, Valor_Reservado, Valor_Empenhado, Valor_Liquidado, ID_Comp
# Capacitações: Nível_Capacitação, Modalidade, Carga_Horária, Vagas_Ofertadas
# Etapas: SEI_DOD, Responsável_DOD, SEI_Financeiro, Responsável_Financeiro, Data_DOD, Data_ETP, Data_PB/TR, Data_Pregão, Data_Assinatura_Contrato, Data_Encerramento_Contrato
# Seleções:  SEI_Seleção, Responsável_Seleção
# Descartados:  Coordenação,




