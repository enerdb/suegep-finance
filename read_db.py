import pandas as pd
import re
from drive import get_sheet_from_drive, get_df_from_drive, update_worksheet_from_df

###############################
# Helper Functions
###############################

def brl_para_float(valor_str: str) -> float:
    """
    Converte uma string representando um valor em reais para float.
    """
    valor_str = re.sub(r'[^\d,.-]', '', valor_str)

    if ',' in valor_str:
        valor_str = valor_str.replace('.', '')  
        valor_str = valor_str.replace(',', '.')  

    if valor_str == '':
        valor_str = '0'  

    try:
        return float(valor_str)
    except ValueError:
        raise ValueError(f"Valor inválido para conversão: '{valor_str}'")


def ajusta_dados_financeiros(coluna: pd.Series) -> pd.Series:
    return coluna.fillna(0).astype(str).apply(brl_para_float).astype(float)


def ajusta_dados_financeiros_df(df: pd.DataFrame, colunas: list) -> pd.DataFrame:
    for col in colunas:
        if col in df.columns:
            df[col] = ajusta_dados_financeiros(df[col])
    return df


def ajusta_datetime_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
    return df


def ajusta_boolean_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            if not pd.api.types.is_bool_dtype(df[col]):
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.lower()
                    .map({'sim': True, 'não': False, 'true': True, 'false': False, '1': True, '0': False})
                )
    return df

###############################
# Tratamento de tabelas
###############################

def trata_repasses(df):
    colunas_financeiras = ['Valor_Repasse_Inicial', 'Ajustes_Soma', 'Valor_Repasse_Atual']
    df = ajusta_dados_financeiros_df(df, colunas_financeiras)

    df['Ano_Repasse'] = pd.to_numeric(df['Ano_Repasse'], errors='coerce').fillna(0).astype(int)
    df['Fonte'] = df['Fonte'].astype(str)
    df['Eixo'] = df['Eixo'].astype(str)
    df['Natureza'] = df['Natureza'].astype(str)
    df['SEI'] = df['SEI'].fillna('').astype(str)

    return df.set_index('id_Repasse')


def trata_repasses_alteracoes(df):
    colunas_financeiras = ['Valor_Ajuste']
    colunas_datetime = ['Data_Ajuste']
    df = ajusta_dados_financeiros_df(df, colunas_financeiras)
    df = ajusta_datetime_columns(df, colunas_datetime)
    if 'index' in df.columns:
        df = df.drop(columns=['index'])
    return df.reset_index(drop=True)


def trata_projetos(df):
    colunas_financeiras = ['Valor_Planejado_Inicial', 'Ajustes_Soma', 'Valor_Planejado_Atual']
    df = ajusta_dados_financeiros_df(df, colunas_financeiras)
    return df.set_index('id_Projeto')


def trata_projetos_alteracoes(df):
    colunas_financeiras = ['Valor_Ajuste']
    df = ajusta_dados_financeiros_df(df, colunas_financeiras)
    if 'index' in df.columns:
        df = df.drop(columns=['index'])
    return df.reset_index(drop=True)


def trata_acoes(df):
    colunas_datetime = ['Data_Início_Planejado', 'Data_Fim_Planejado', 'Data_Início_Real', 'Data_Fim_Real']
    df = ajusta_datetime_columns(df, colunas_datetime)
    return df.set_index('id_Ação')


def trata_contratacoes(df):
    colunas_financeiras = ['Valor_Reservado', 'Valor_Empenhado', 'Valor_Liquidado']
    colunas_datetime = ['Data_Contrato', 'Data_Encerramento_Contrato']
    df = ajusta_dados_financeiros_df(df, colunas_financeiras)
    df = ajusta_datetime_columns(df, colunas_datetime)
    return df.set_index('id_Contratação')


def trata_etapa_contratacao(df):
    colunas_datetime = ['Data_início_etapa', 'Data_fim_etapa']
    df = ajusta_datetime_columns(df, colunas_datetime)
    return df.set_index('id_Etapa')


def trata_capacitacoes(df):
    colunas_datetime = ['Data_Início_Planejado', 'Data_Fim_Planejado', 'Data_Início_Real', 'Data_Fim_Real']
    df = ajusta_datetime_columns(df, colunas_datetime)
    return df.set_index('id_Capacitação')


def trata_selecoes(df):
    return df.set_index('id_Seleção')


def trata_inscricoes(df):
    colunas_bool = ['Matriculado', 'Concluinte']
    df = ajusta_boolean_columns(df, colunas_bool)
    return df.set_index('id_inscrição')


def trata_inscricoes_moodle(df):
    return df.set_index('id_inscrição')


def trata_metas(df):
    return df.set_index('id_Meta')  # ainda não implementado


def trata_apoio(df):
    return df  # ainda não implementado


###############################
# Importação do Google Drive
###############################

def read_db_drive():
    spreadsheet = get_sheet_from_drive('BI_db')
    return {
        'Repasses': trata_repasses(get_df_from_drive(spreadsheet, 'Repasses')),
        'Repasses_Alterações': trata_repasses_alteracoes(get_df_from_drive(spreadsheet, 'Repasses_Alterações')),
        'Projetos': trata_projetos(get_df_from_drive(spreadsheet, 'Projetos')),
        'Projetos_Alterações': trata_projetos_alteracoes(get_df_from_drive(spreadsheet, 'Projetos_Alterações')),
        'Ações': trata_acoes(get_df_from_drive(spreadsheet, 'Ações')),
        'Contratações': trata_contratacoes(get_df_from_drive(spreadsheet, 'Contratações')),
        'Etapa_Contratação': trata_etapa_contratacao(get_df_from_drive(spreadsheet, 'Etapa_Contratação')),
        'Capacitações': trata_capacitacoes(get_df_from_drive(spreadsheet, 'Capacitações')),
        'Seleções': trata_selecoes(get_df_from_drive(spreadsheet, 'Seleções')),
        'Inscrições': trata_inscricoes(get_df_from_drive(spreadsheet, 'Inscrições')),
        'Inscrições_Moodle': trata_inscricoes_moodle(get_df_from_drive(spreadsheet, 'Inscrições_Moodle')),
        'Metas': trata_metas(get_df_from_drive(spreadsheet, 'Metas')),
        # 'Apoio': trata_apoio(get_df_from_drive(spreadsheet, 'Apoio')),
    }

###############################
# Importação de Excel
###############################

def read_db_excel(path: str):
    return {
        'Repasses': trata_repasses(pd.read_excel(path, sheet_name='Repasses')),
        'Repasses_Alterações': trata_repasses_alteracoes(pd.read_excel(path, sheet_name='Repasses_Alterações')),
        'Projetos': trata_projetos(pd.read_excel(path, sheet_name='Projetos')),
        'Projetos_Alterações': trata_projetos_alteracoes(pd.read_excel(path, sheet_name='Projetos_Alterações')),
        'Ações': trata_acoes(pd.read_excel(path, sheet_name='Ações')),
        'Contratações': trata_contratacoes(pd.read_excel(path, sheet_name='Contratações')),
        'Etapa_Contratação': trata_etapa_contratacao(pd.read_excel(path, sheet_name='Etapa_Contratação')),
        'Capacitações': trata_capacitacoes(pd.read_excel(path, sheet_name='Capacitações')),
        'Seleções': trata_selecoes(pd.read_excel(path, sheet_name='Seleções')),
        'Inscrições': trata_inscricoes(pd.read_excel(path, sheet_name='Inscrições')),
        'Inscrições_Moodle': trata_inscricoes_moodle(pd.read_excel(path, sheet_name='Inscrições_Moodle')),
        'Metas': trata_metas(pd.read_excel(path, sheet_name='Metas')),
        # 'Apoio': trata_apoio(pd.read_excel(path, sheet_name='Apoio')),
    }

###############################
# Utilitário para impressão
###############################

def print_db(bi_db, format='console'):
    if format == 'console':
        print_funcion = print
    elif format == 'streamlit':
        import streamlit as st
        print_funcion = st.write
        
    for key, value in bi_db.items():
        print_funcion(f"{key} ({value.shape[0]} linhas, {value.shape[1]} colunas)")
        print_funcion(value.dtypes)
        print_funcion(value.head())
        print_funcion("\n")

def update_db_drive(bi_db):
    spreadsheet = get_sheet_from_drive('BI_db')

    update_worksheet_from_df(spreadsheet.worksheet('Repasses'), bi_db['Repasses'])
    update_worksheet_from_df(spreadsheet.worksheet('Repasses_Alterações'), bi_db['Repasses_Alterações']) # teste
    update_worksheet_from_df(spreadsheet.worksheet('Projetos'), bi_db['Projetos'])
    update_worksheet_from_df(spreadsheet.worksheet('Projetos_Alterações'), bi_db['Projetos_Alterações']) # teste
    update_worksheet_from_df(spreadsheet.worksheet('Ações'), bi_db['Ações'])
    update_worksheet_from_df(spreadsheet.worksheet('Contratações'), bi_db['Contratações'])
    update_worksheet_from_df(spreadsheet.worksheet('Etapa_Contratação'), bi_db['Etapa_Contratação'])
    update_worksheet_from_df(spreadsheet.worksheet('Capacitações'), bi_db['Capacitações'])
    update_worksheet_from_df(spreadsheet.worksheet('Seleções'), bi_db['Seleções'])
    update_worksheet_from_df(spreadsheet.worksheet('Inscrições'), bi_db['Inscrições'])
    update_worksheet_from_df(spreadsheet.worksheet('Inscrições_Moodle'), bi_db['Inscrições_Moodle'])
    update_worksheet_from_df(spreadsheet.worksheet('Metas'), bi_db['Metas'])