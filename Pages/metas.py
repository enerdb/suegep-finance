
import streamlit as st
import time
import pandas as pd
import config

from sidebar import render_sidebar

from tools.format_df import formatar_df_datas

#########################################
# CARGA DE DADOS
#########################################

if 'bi_db' not in st.session_state:
    st.error("Dados não carregados. Por favor, volte para a página inicial e carregue os dados.")
    st.stop()

render_sidebar()

df_selecoes_filtered = st.session_state.filtered_db['Metas']

#########################################
# FILTRAGEM E EXIBIÇÃO PARA EXIBIÇÃO
#########################################

st.markdown("### Exibição de Metas")

df_display = df_selecoes_filtered
st.dataframe(df_display)