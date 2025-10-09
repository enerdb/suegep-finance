import streamlit as st
import pandas as pd
from config import TABELAS_CONFIG, SAVE2SHEETS

from sidebar import render_sidebar

from tools.format_df import formatar_df_datas
from tools.crud_table import exibir_tabela, formulario_generico, formulario_exclusao


#########################################
# CARGA DE DADOS
#########################################

if 'bi_db' not in st.session_state:
    st.error("Dados não carregados. Por favor, volte para a página inicial e carregue os dados.")
    st.stop()

render_sidebar()

tabela_nome = 'Capacitações'
config_tabela = TABELAS_CONFIG[tabela_nome]



#########################################
# FILTRAGEM E EXIBIÇÃO PARA EXIBIÇÃO
#########################################

df_capacitacoes_filtered = st.session_state['filtered_db']['Capacitações']

st.markdown("### Exibição de Capacitações")

exibir_tabela(df_capacitacoes_filtered,
              cols_datas=config_tabela['cols_datas'],
              cols_monetarios=config_tabela['cols_monetarios'])

#########################################
# FORMULÁRIO PARA ADICIONAR NOVA CAPACITAÇÃO
#########################################

# Adicionar capacitação
formulario_generico(tabela_nome, df_capacitacoes_filtered, config_tabela['campos'], config_tabela['chave_primaria'])

# Excluir capacitação
formulario_exclusao(tabela_nome, df_capacitacoes_filtered)