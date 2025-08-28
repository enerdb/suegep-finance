
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

df_selecoes_filtered = st.session_state.filtered_db['Seleções']

#########################################
# FILTRAGEM E EXIBIÇÃO PARA EXIBIÇÃO
#########################################

st.markdown("### Exibição de Seleções")

cols_datas = ['Data_Início_Planejado', 'Data_Fim_Planejado', 'Data_Início_Real', 'Data_Fim_Real']
df_display = formatar_df_datas(df_selecoes_filtered, cols_datas)
st.dataframe(df_display)