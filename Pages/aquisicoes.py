import streamlit as st
import pandas as pd
from config import TABELAS_CONFIG, SAVE2SHEETS

from sidebar import render_sidebar
from tools.crud_table import exibir_tabela, formulario_generico, formulario_exclusao

#########################################
# CARGA DE DADOS
#########################################

if 'bi_db' not in st.session_state:
    st.error("Dados não carregados. Por favor, volte para a página inicial e carregue os dados.")
    st.stop()

render_sidebar()

tabela_nome = 'Aquisições'
config_tabela = TABELAS_CONFIG[tabela_nome]

#########################################
# FILTRAGEM E EXIBIÇÃO PARA EXIBIÇÃO
#########################################

df_metas_filtered = st.session_state.filtered_db[tabela_nome]

exibir_tabela(df_metas_filtered,
              cols_datas=config_tabela['cols_datas'],
              cols_monetarios=config_tabela['cols_monetarios'])

#########################################
# FORMULÁRIO PARA ADICIONAR NOVA CONTRATAÇÃO
#########################################

# Adicionar aquisição       
formulario_generico(tabela_nome, df_metas_filtered, config_tabela['campos'], config_tabela['chave_primaria'])

# Excluir aquisição
formulario_exclusao(tabela_nome, df_metas_filtered)