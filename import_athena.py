import streamlit as st
import pandas as pd
from drive import get_sheet_from_drive, get_df_from_drive, update_worksheet_from_df
import re

############################
# Helper functions
###

import re

def limpar_e_validar_cpf(cpf: str) -> bool:
    """
    Remove caracteres não numéricos, preenche com zeros à esquerda se necessário,
    e valida se a string resultante é um CPF brasileiro válido.

    Parâmetros:
        cpf (str): String contendo o CPF (com ou sem formatação).

    Retorna:
        bool: True se for um CPF válido, False caso contrário.
    """
    # Remove tudo que não é dígito
    cpf_numeros = re.sub(r'\D', '', cpf)

    # Preenche com zeros à esquerda até ter 11 caracteres
    cpf_numeros = cpf_numeros.zfill(11)

    # Verifica se tem exatamente 11 dígitos
    if len(cpf_numeros) != 11:
        return False

    # Descarta CPFs com todos os dígitos iguais
    if cpf_numeros == cpf_numeros[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    soma1 = sum(int(cpf_numeros[i]) * (10 - i) for i in range(9))
    digito1 = (soma1 * 10 % 11) % 10

    # Calcula o segundo dígito verificador
    soma2 = sum(int(cpf_numeros[i]) * (11 - i) for i in range(10))
    digito2 = (soma2 * 10 % 11) % 10

    # Compara com os dígitos fornecidos
    return cpf_numeros[-2:] == f"{digito1}{digito2}"

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

def ajusta_datetime_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Ajusta as colunas de data de um DataFrame, convertendo-as para o tipo datetime.
    Se a coluna não for do tipo datetime, converte usando o formato brasileiro (dia/mês/ano).
    """
    for col in columns:
        if col in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce').dt.date
    return df

############################
# # Funções de importação de dados
###

def importa_repasses():
    df = pd.read_excel('data\TbPadronizada.xlsx', 0)
    df.columns = ['id_Repasse', 'Ano_Repasse', 'Fonte', 'Eixo', 'Natureza', 'Valor_Repasse_Inicial']
    df['Valor_Repasse_Inicial'] = ajusta_dados_financeiros(df['Valor_Repasse_Inicial'])
    df['Ajustes_Soma'] = None
    df['Ajustes_Soma'] = ajusta_dados_financeiros(df['Ajustes_Soma'])
    df['Valor_Repasse_Autual'] = df['Valor_Repasse_Inicial'] + df['Ajustes_Soma']
    df['SEI'] = None
    df['SEI'] = df['SEI'].fillna('')
    return df.set_index('id_Repasse')

def importa_projetos():
    df = pd.read_excel('data\TbPadronizada.xlsx', 1)
    df = df.rename(columns={'PR_ID': 'id_Projeto', 'Projeto': 'Nome_Projeto', 'Planejado (R$)': 'Valor_Planejado_Inicial', 'RP_ID': 'id_Repasse'})
    df = df[['id_Projeto', 'id_Repasse', 'Nome_Projeto', 'Valor_Planejado_Inicial',]]
    
    df['Valor_Planejado_Inicial'] = ajusta_dados_financeiros(df['Valor_Planejado_Inicial'])
    df['Ajustes_Soma'] = None
    df['Ajustes_Soma'] = ajusta_dados_financeiros(df['Ajustes_Soma'])
    df['Valor_Planejado_Atual'] = df['Valor_Planejado_Inicial'] + df['Ajustes_Soma']
    return df.set_index('id_Projeto')

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
    
    df = ajusta_datetime_columns(df, date_columns)
    
    df['Status'] = None
    df['Histórico'] = None
    df['Histórico'] = df['Histórico'].fillna('')

    # Filtrar e retornar apenas as colunas que são usadas
    colunas_usadas = ['id_Ação', 'id_Projeto', 'Nome_Ação', 'Tipo_Ação', 
                     'Data_Início_Planejado', 'Data_Fim_Planejado', 
                     'Data_Início_Real', 'Data_Fim_Real', 'Status', 'Histórico']

    return df[colunas_usadas].set_index('id_Ação')

def importa_contratacoes():
    df = pd.read_excel('data\TbPadronizada.xlsx', 2)
    df = df.rename(columns={'ID_Comp': 'id_Contratação', # Substituira aqui pelo código do Almada
                            'AC_ID': 'id_Ação',
                            'CNPJ' : 'CNPJ_Contratada',
                            'Contratada': 'Nome_Contratada',
                            'Data_Assinatura_Contrato': 'Data_Contrato',
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
        elif pd.notna(row['Data_Contrato']):
            return 'Execução'
        elif pd.notna(row['Data_PB/TR']):
            return 'Contratação'
        else:
            return 'Planejamento'
    df['Etapa_Atual'] = df.apply(determine_etapa, axis=1)

    # Converter valores financeiros de BRL para float
    df['Valor_Reservado'] = ajusta_dados_financeiros(df['Valor_Reservado'])
    df['Valor_Empenhado'] = ajusta_dados_financeiros(df['Valor_Empenhado'])
    df['Valor_Liquidado'] = ajusta_dados_financeiros(df['Valor_Liquidado'])

    date_columns = ['Data_Contrato', 'Data_Encerramento_Contrato']
    df = ajusta_datetime_columns(df, date_columns)
    
    colunas_usadas = ['id_Contratação', 'id_Ação', 'CNPJ_Contratada', 'Nome_Contratada', 'Data_Contrato', 'Data_Encerramento_Contrato', 'Valor_Reservado', 'Valor_Empenhado', 'Valor_Liquidado', 'Etapa_Atual']

    return df[colunas_usadas].set_index('id_Contratação')
    

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
        id_acao = row['AC_ID']

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
    datetima_columns = ['Data_início_etapa', 'Data_fim_etapa']

    df_etapas = ajusta_datetime_columns(df_etapas, datetima_columns)

    return df_etapas.set_index('id_Etapa')

def importa_capacitacoes():
    df  = pd.read_excel('data\TbPadronizada.xlsx', 2)
    df = df.rename(columns={'ID_Comp': 'id_Capacitação', # Definir
                            'AC_ID': 'id_Ação',
                            'Ação': 'Nome_Capacitação',
                            'Contratada': 'Nome_Escola',
                            'Nível_Capacitação':'Nível_Capacitação',
                            'Modalidade': 'Modalidade_Capacitação',
                            'Carga_Horária': 'Carga_Horária_Horas',
                            'Vagas_Ofertadas': 'Vagas_Ofertadas',
                            'Data_Início_Ação': 'Data_Início_Real',
                            'Data_Término_Ação': 'Data_Fim_Real',
                            })
    df['Data_Início_Planejado'] = df['Data_Início_Real']
    df['Data_Fim_Planejado'] = df['Data_Fim_Real']

    date_columns = ['Data_Início_Planejado', 'Data_Fim_Planejado', 'Data_Início_Real', 'Data_Fim_Real']
    df = ajusta_datetime_columns(df, date_columns)

    colunas_usadas = ['id_Capacitação', 'id_Ação', 'Nome_Capacitação', 'Nome_Escola',
                     'Nível_Capacitação', 'Modalidade_Capacitação', 
                     'Carga_Horária_Horas', 'Vagas_Ofertadas', 
                     'Data_Início_Planejado', 'Data_Fim_Planejado', 
                     'Data_Início_Real', 'Data_Fim_Real']
    return df[colunas_usadas].set_index('id_Capacitação')

def importa_selecoes():
    df = pd.read_excel('data\TbPadronizada.xlsx', 2)
    df = df.rename(columns={'ID_Comp': 'id_Capacitação', # Definir
                             'Responsável_Seleção': 'Responsável_Seleção',
                             'SEI_Seleção': 'SEI_Seleção' ,})
    df = df.dropna(subset=['Responsável_Seleção', 'SEI_Seleção'], how='all').reset_index(drop=True)

    df=df.rename_axis('id_Seleção')
    return df[['id_Capacitação', 'Responsável_Seleção', 'SEI_Seleção']]
    
def importa_inscricoes():
    df= pd.read_excel('data\TbPadronizada.xlsx', 3)
    df_acoes = pd.read_excel('data\TbPadronizada.xlsx', 2)

    mapa_acoes = dict(zip(df_acoes['AC_ID'], df_acoes['ID_Comp']))
    
    df = df.rename(columns={'AC_ID': 'id_Acao',
                            'CPF': 'CPF',
                            'Matriculado': 'Matriculado',
                            'Concluinte': 'Concluinte'})
    
    df['CPF'] = df['CPF'].astype(str).str.replace(r'\D', '', regex=True)  # Limpar CPF, removendo caracteres não numéricos
    df['CPF_válido'] = df['CPF'].apply(limpar_e_validar_cpf)  # Validar CPF

    
    df['id_Capacitação'] = df['id_Acao'].map(mapa_acoes)
    df=df.rename_axis('id_inscrição')

    return df[['id_Capacitação', 'CPF', 'Matriculado', 'Concluinte']]
    
def importa_inscricao_moodle():
    df= pd.read_excel('data\TbPadronizada.xlsx', 3)
    df_acoes = pd.read_excel('data\TbPadronizada.xlsx', 2)

# Inscrições_Moodle: [id_Inscrição], Axis
# AC_ID (Id_capacitação), map
# CPF, Nome_Completo, Sexo, [Data_Nascimento], Orgao_Origem, Lotacao_Atual, [Setor, Telefone1, Telefone2, email1, email2, situação_funcional, carreira, Área_Atuação] , Chefe_imediato, Chefe_imediato_contato



    mapa_acoes = dict(zip(df_acoes['AC_ID'], df_acoes['ID_Comp']))
    
    df = df.rename(columns={'AC_ID': 'id_Acao',
                            'CPF': 'CPF',
                            'Nome_Completo': 'Nome_Completo',
                            'Sexo': 'Sexo',
                            'Orgao_Origem': 'Orgao_Origem',
                            'Lotacao_Atual': 'Lotacao'
                            })
    
    df['CPF'] = df['CPF'].astype(str).str.replace(r'\D', '', regex=True)  # Limpar CPF, removendo caracteres não numéricos
    df['CPF_válido'] = df['CPF'].apply(limpar_e_validar_cpf)  # Validar CPF

    df['id_Capacitação'] = df['id_Acao'].map(mapa_acoes)

    df['Data_Nascimento'] = None
    df['Setor'] = None
    df['Telefone1'] = None
    df['Telefone2'] = None
    df['email1'] = None
    df['email2'] = None
    df['situação_funcional'] = None
    df['carreira'] = None
    df['Área_Atuação'] = None
    df['Chefe_imediato'] = None
    df['Chefe_imediato_contato'] = None

    df=df.rename_axis('id_inscrição')

    return df[['id_Capacitação', 'CPF', 'Nome_Completo', 'Sexo', 'Data_Nascimento', 'Orgao_Origem', 'Lotacao',
               'Setor', 'Telefone1', 'Telefone2', 'email1', 'email2', 'situação_funcional', 'carreira', 'Área_Atuação',
               'Chefe_imediato', 'Chefe_imediato_contato']]  

class ExcelAthena:
    """Classe para importar e armazenar as tabelas do Excel Athena"""
    
    def __init__(self):
        self.repasses = importa_repasses()
        self.projetos = importa_projetos()
        self.acoes = importa_acoes()
        self.contratacoes = importa_contratacoes()
        self.etapas = importa_etapas()
        self.capacitacoes = importa_capacitacoes()
        self.selecoes = importa_selecoes()
        self.inscricoes = importa_inscricoes()
        self.inscricao_moodle = importa_inscricao_moodle()

    def print_tabelas_streamlit(self):
        """Imprime todas as tabelas importadas"""

        for attribute, value in self.__dict__.items():
            st.write(f"**{attribute}**")
            st.write(value.dtypes)  # Exibe os tipos de dados das colunas
            st.write(value)

    

if __name__ == "__main__":
    st.set_page_config(
        page_title="Importação Athena",
        page_icon=":bar_chart:",
        layout="wide")
    if 'excel' not in st.session_state:
        st.session_state.excel = ExcelAthena()

    st.title("Importação Athena")
    st.write("Este aplicativo importa e exibe as tabelas do Excel Athena.") 
    with st.expander("Tabelas Importadas", expanded=True):
        st.session_state.excel.print_tabelas_streamlit()


    print("******************************************************************************************************")


    spreadsheet = get_sheet_from_drive('BI_db')

    update_worksheet_from_df(spreadsheet.worksheet('Repasses'), st.session_state.excel.repasses)
    update_worksheet_from_df(spreadsheet.worksheet('Projetos'), st.session_state.excel.projetos)
    update_worksheet_from_df(spreadsheet.worksheet('Ações'), st.session_state.excel.acoes, debug=True)
    update_worksheet_from_df(spreadsheet.worksheet('Contratações'), st.session_state.excel.contratacoes)
    update_worksheet_from_df(spreadsheet.worksheet('Etapa_Contratação'), st.session_state.excel.etapas)
    update_worksheet_from_df(spreadsheet.worksheet('Capacitações'), st.session_state.excel.capacitacoes)
    update_worksheet_from_df(spreadsheet.worksheet('Seleções'), st.session_state.excel.selecoes)
    update_worksheet_from_df(spreadsheet.worksheet('Inscrições'), st.session_state.excel.inscricoes)
    update_worksheet_from_df(spreadsheet.worksheet('Inscrições_Moodle'), st.session_state.excel.inscricao_moodle)
    st.success("Dados importados e atualizados com sucesso!")
    






###
# Modelagem athena
# TB_Acoes:
# AC_ID, Ação, SEI_DOD, Responsável_DOD, Coordenação, Tipo_de_ação, Nível_Capacitação, Modalidade, Carga_Horária, Vagas_Ofertadas, SEI_Seleção, Responsável_Seleção, Data_Início_Ação, Data_Término_Ação, SEI_Financeiro, Responsável_Financeiro, CNPJ, Contratada, Data_DOD, Data_ETP, Data_PB/TR, Data_Pregão, Data_Assinatura_Contrato, Data_Encerramento_Contrato, Valor_Reservado, Valor_Empenhado, Valor_Liquidado, PR_ID, ID_Comp
#   
# TB_Participantes:
# AC_ID, CPF, Nome_Completo, Sexo, Orgao_Origem, Lotacao_Atual, Matriculado, Concluinte
#
# TB_Meta_Projeto:
# PR_ID,	Indicador,	Meta,	SEI_Prest_Contas,	Resp_Prest_Contas,	Data_C_Meta,	Obs
# 
# TB_R_Capacitados:
# AC_ID,	T_Inscritos,	T_Matriculados,	T_Concluintes


# Transposição Modelagem nova TB_Acoes
# Ações: AC_ID, PR_ID, Ação, Tipo_de_ação, Data_Início_Ação, Data_Término_Ação
# Contratações: CNPJ, Contratada, Valor_Reservado, Valor_Empenhado, Valor_Liquidado, ID_Comp
# Capacitações: Nível_Capacitação, Modalidade, Carga_Horária, Vagas_Ofertadas
# Etapas: SEI_DOD, Responsável_DOD, SEI_Financeiro, Responsável_Financeiro, Data_DOD, Data_ETP, Data_PB/TR, Data_Pregão, Data_Assinatura_Contrato, Data_Encerramento_Contrato
# Seleções:  SEI_Seleção, Responsável_Seleção
# Descartados:  Coordenação,

# Transposição Modelagem nova TB_Participantes
# Inscrições: [id_Inscrição], AC_ID (Id_capacitação), CPF, Matriculado, Concluinte
# Inscrições_Moodle: [id_Inscrição], AC_ID (Id_capacitação), CPF, Nome_Completo, Sexo, [Data_Nascimento], Orgao_Origem, Lotacao_Atual, [Setor, Telefone1, Telefone2, email1, email2, situação_funcional, carreira, Área_Atuação] , Chefe_imediato, Chefe_imediato_contato



