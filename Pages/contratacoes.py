import streamlit as st
import pandas as pd
from config import TABELAS_CONFIG, SAVE2SHEETS

from sidebar import render_sidebar
from form_functions import excluir_item

from tools.crud_table import exibir_tabela, formulario_generico, formulario_exclusao


from tools.format_df import formatar_df_reais, formatar_df_datas

#########################################
# CARGA DE DADOS
#########################################

if 'bi_db' not in st.session_state:
    st.error("Dados não carregados. Por favor, volte para a página inicial e carregue os dados.")
    st.stop()

save2sheets = SAVE2SHEETS

render_sidebar()

tabela_nome = 'Contratações'

config_tabela = TABELAS_CONFIG[tabela_nome]



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
exibir_tabela(df_contratacoes_filtered,
              cols_datas=config_tabela['cols_datas'],
              cols_monetarios=config_tabela['cols_monetarios'])

#########################################
# FORMULÁRIO PARA ADICIONAR NOVA CONTRATAÇÃO
#########################################

# Adicionar contratção
formulario_generico(tabela_nome, df_contratacoes_filtered, config_tabela['campos'], config_tabela['chave_primaria'])

# Excluir contratação
formulario_exclusao(tabela_nome, df_contratacoes_filtered)

