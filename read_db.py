import pandas as pd
from drive import get_sheet_from_drive, get_df_from_drive
import re

##############################
# Helper Functions
###############################


def brl_para_float(valor_str: str) -> float:
    """
    Converte uma string representando um valor em reais para float.
    Suporta formatos com ou sem "R$", com vírgula ou ponto decimal.

    Exemplos válidos:
        "R$ 5.650,00" → 5650.0
        "5650,00"     → 5650.0
        "5650.00"     → 5650.0
        "R$5650"      → 5650.0
        "1000"        → 1000.0
    """
    # Remove tudo que não for número, vírgula, ponto ou sinal
    valor_str = re.sub(r'[^\d,.-]', '', valor_str)

    # Se a vírgula estiver presente, assume que é separador decimal brasileiro
    if ',' in valor_str:
        valor_str = valor_str.replace('.', '')  # remove pontos de milhar
        valor_str = valor_str.replace(',', '.') # converte separador decimal para ponto
    # Se não tiver vírgula, assume que ponto (se existir) já é decimal

    if valor_str == '':
        valor_str = '0'  # Se a string estiver vazia, define como zero

    try:
        return float(valor_str)
    except ValueError:
        raise ValueError(f"Valor inválido para conversão: '{valor_str}'")

def ajusta_dados_financeiros(coluna: pd.Series) -> pd.Series:
    """
    Ajusta os dados financeiros de uma coluna, convertendo valores em reais para float.
    Se o valor for NaN, retorna 0.0.
    """
    return coluna.fillna(0).astype(str).apply(brl_para_float).astype(float)

def ajusta_dados_financeiros_df(df: pd.DataFrame, colunas: list) -> pd.DataFrame:
    """
    Ajusta as colunas de dados financeiros de um DataFrame, convertendo valores em reais para float.
    Se o valor for NaN, retorna 0.0.
    """
    for col in colunas:
        if col in df.columns:
            df[col] = ajusta_dados_financeiros(df[col])
    return df

def ajusta_datetime_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Ajusta as colunas de data de um DataFrame, convertendo-as para o tipo datetime.
    Se a coluna não for do tipo datetime, converte usando o formato brasileiro (dia/mês/ano).
    """
    for col in columns:
        if col in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df[col]):
                #df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce').dt.date
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
    return df

def ajusta_boolean_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Ajusta as colunas booleanas de um DataFrame, convertendo-as para o tipo booleano.
    Se a coluna não for do tipo booleano, converte usando uma lógica simples.
    """
    for col in columns:
        if col in df.columns:
            if not pd.api.types.is_bool_dtype(df[col]):
                df[col] = df[col].astype(str).str.lower().map({'sim': True, 'não': False, 'true': True, 'false': False, '1': True, '0': False})
    return df

##############################
# Reading Functions
###############################

# Tabs = Repasses, Repasses_Alterações, Projetos, Projetos_Alterações, Ações, Contratações, Etapa_Contratação, Capacitações, Seleções, Inscrições, Inscrições_Moodle, Apoio

def read_repasses(spreadsheet):
    
    # Cols: id_Repasse	Ano_Repasse	Fonte	Eixo	Natureza	Valor_Repasse_Inicial	Ajustes_Soma	Valor_Repasse_Atual	SEI
    colunas_financeiras = ['Valor_Repasse_Inicial', 'Ajustes_Soma', 'Valor_Repasse_Atual']
    
    df = get_df_from_drive(spreadsheet, 'Repasses')
    df = ajusta_dados_financeiros_df(df, colunas_financeiras)
     
    return df.set_index('id_Repasse')

def read_repasses_alteracoes(spreadsheet):
    # Cols: id_Repasse	Evento	Valor_Ajuste	SEI     Data_Ajuste

    colunas_financeiras = ['Valor_Ajuste']
    colunas_datetime = ['Data_Ajuste'] 

    df = get_df_from_drive(spreadsheet, 'Repasses_Alterações')
    df = ajusta_dados_financeiros_df(df, colunas_financeiras)
    df = ajusta_datetime_columns(df, colunas_datetime)
    
    #return df.set_index('id_Repasse')
    return df

def read_projetos(spreadsheet):
    # cols: id_Projeto	id_Repasse	Nome_Projeto	Valor_Planejado_Inicial	Ajustes_Soma	Valor_Planejado_Atual

    colunas_financeiras = ['Valor_Planejado_Inicial', 'Ajustes_Soma', 'Valor_Planejado_Atual']

    df = get_df_from_drive(spreadsheet, 'Projetos')
    df = ajusta_dados_financeiros_df(df, colunas_financeiras)
    
    return df.set_index('id_Projeto')

def read_projetos_alteracoes(spreadsheet):
    # Cols: id_Projeto	Evento	Valor_Ajuste	SEI

    colunas_financeiras = ['Valor_Ajuste']
    df = get_df_from_drive(spreadsheet, 'Projetos_Alterações')
    df = ajusta_dados_financeiros_df(df, colunas_financeiras)

    #return df.set_index('id_Projeto')
    return df

def read_acoes(spreadsheet):
    #Cols: id_Ação	id_Projeto	Nome_Ação	Tipo_Ação	Data_Início_Planejado	Data_Fim_Planejado	Data_Início_Real	Data_Fim_Real	Status	Histórico
    colunas_datetime = ['Data_Início_Planejado', 'Data_Fim_Planejado', 'Data_Início_Real', 'Data_Fim_Real']
    
    df = get_df_from_drive(spreadsheet, 'Ações')
    df = ajusta_datetime_columns(df, colunas_datetime)
    
    return df.set_index('id_Ação')

def read_contratacoes(spreadsheet):
    # Cols: id_Contratação	id_Ação	CNPJ_Contratada	Nome_Contratada	Data_Contrato	Data_Encerramento_Contrato	Valor_Reservado	Valor_Empenhado	Valor_Liquidado	Etapa_Atual
    colunas_financeiras = ['Valor_Reservado', 'Valor_Empenhado', 'Valor_Liquidado']
    colunas_datetime = ['Data_Contrato', 'Data_Encerramento_Contrato']  
    
    df = get_df_from_drive(spreadsheet, 'Contratações')
    df = ajusta_dados_financeiros_df(df, colunas_financeiras)
    df = ajusta_datetime_columns(df, colunas_datetime)

    return df.set_index('id_Contratação')

def read_etapa_contratacao(spreadsheet):
    # Cols: id_Etapa	idAcao	tipo_etapa	SEI	Responsável	Data_início_etapa	Data_fim_etapa

    colunas_datetime = ['Data_início_etapa', 'Data_fim_etapa']
    df = get_df_from_drive(spreadsheet, 'Etapa_Contratação')
    df = ajusta_datetime_columns(df, colunas_datetime)

    return df.set_index('id_Etapa')

def read_capacitacoes(spreadsheet):
    #Cols: id_Capacitação	id_Ação	Nome_Capacitação	Nome_Escola	Nível_Capacitação	Modalidade_Capacitação	Carga_Horária_Horas	Vagas_Ofertadas	Data_Início_Planejado	Data_Fim_Planejado	Data_Início_Real	Data_Fim_Real
    colunas_datetime = ['Data_Início_Planejado', 'Data_Fim_Planejado', 'Data_Início_Real', 'Data_Fim_Real']
        
    df = get_df_from_drive(spreadsheet, 'Capacitações')
    df = ajusta_datetime_columns(df, colunas_datetime)

    return df.set_index('id_Capacitação')

def read_selecoes(spreadsheet):
    #Cols: id_Seleção	id_Capacitação	Responsável_Seleção	SEI_Seleção
    df = get_df_from_drive(spreadsheet, 'Seleções')
    
    return df.set_index('id_Seleção')

def read_inscricoes(spreadsheet):
    # Cols: id_inscrição	id_Capacitação	CPF	Matriculado	Concluinte
    colunas_bool = ['Matriculado', 'Concluinte']
    
    df = get_df_from_drive(spreadsheet, 'Inscrições')
    df = ajusta_boolean_columns(df, colunas_bool)

    return df.set_index('id_inscrição')

def read_inscricoes_moodle(spreadsheet):
    # Cols: id_inscrição	id_Capacitação	CPF	Nome_Completo	Sexo	Data_Nascimento	Orgao_Origem	Lotacao	Setor	Telefone1	Telefone2	email1	email2	situação_funcional	carreira	Área_Atuação	Chefe_imediato	Chefe_imediato_contato

    df = get_df_from_drive(spreadsheet, 'Inscrições_Moodle')
    
    return df.set_index('id_inscrição')

def read_apoio(spreadsheet):
    pass

def read_db():
    """
    Lê os dados do banco de dados BI_db do Google Drive e retorna um dict de Dataframes.
    """
    bi_db = {}
    spreadsheet = get_sheet_from_drive('BI_db')
    bi_db['Repasses'] = read_repasses(spreadsheet)
    bi_db['Repasses_Alterações'] = read_repasses_alteracoes(spreadsheet)
    bi_db['Projetos'] = read_projetos(spreadsheet)
    bi_db['Projetos_Alterações'] = read_projetos_alteracoes(spreadsheet)
    bi_db['Ações'] = read_acoes(spreadsheet)
    bi_db['Contratações'] = read_contratacoes(spreadsheet)
    bi_db['Etapa_Contratação'] = read_etapa_contratacao(spreadsheet)
    bi_db['Capacitações'] = read_capacitacoes(spreadsheet)
    bi_db['Seleções'] = read_selecoes(spreadsheet)
    bi_db['Inscrições'] = read_inscricoes(spreadsheet)
    bi_db['Inscrições_Moodle'] = read_inscricoes_moodle(spreadsheet)

    return bi_db

def print_db(bi_db, format='console'):
    """
    Imprime os DataFrames do banco de dados BI_db.
    """

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

    # for key, value in st.session_state.bi_db.items():
    #     with st.expander(f"{key} ({value.shape[0]} linhas, {value.shape[1]} colunas)", expanded=False):
    #         st.write(f"**{key}**")
    #         st.write(value.dtypes)
    #         st.dataframe(value)

