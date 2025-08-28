import streamlit as st
import time
import pandas as pd
import config

from sidebar import render_sidebar

from tools.format_df import formatar_df_reais, formatar_df_datas

#########################################
# CARGA DE DADOS
#########################################

if 'bi_db' not in st.session_state:
    st.error("Dados não carregados. Por favor, volte para a página inicial e carregue os dados.")
    st.stop()

save2sheets = config.SAVE2SHEETS

render_sidebar()

df_repasses = st.session_state['bi_db']['Repasses']
df_contratos = st.session_state['bi_db']['Contratações']


#########################################
# FILTRAGEM E EXIBIÇÃO PARA EXIBIÇÃO
#########################################

df_repasses_filtered            = st.session_state['filtered_db']['Repasses']
df_projetos_filtered            = st.session_state['filtered_db']['Projetos']
df_acoes_filtered               = st.session_state['filtered_db']['Ações']
df_contratacoes_filtered        = st.session_state.filtered_db['Contratações']


st.markdown("### Exibição de Contratações")

cols_monetarios = ['Valor_Reservado', 'Valor_Empenhado', 'Valor_Liquidado']
cols_datas = ['Data_Contrato', 'Data_Encerramento_Contrato']

df_display = formatar_df_reais(df_contratacoes_filtered, cols_monetarios)
df_display = formatar_df_datas(df_display, cols_datas)

st.dataframe(df_display)