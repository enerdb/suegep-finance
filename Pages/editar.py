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



#########################################
# FILTRAGEM E EXIBIÇÃO PARA EXIBIÇÃO
#########################################

def filter_and_show_table(tabela_nome):

    df_filtered = st.session_state['filtered_db'][tabela_nome]

    st.markdown(f"### Exibição de {tabela_nome}")

    exibir_tabela(df_filtered,
                cols_datas=config_tabela['cols_datas'],
                cols_monetarios=config_tabela['cols_monetarios'])



#########################################
# INTERFACE
#########################################

############
Seleção da planilha

tabela_nome = st.select_box(TABELAS_CONFIG.keys)

if(tabela_nome):
    config_tabela = TABELAS_CONFIG[tabela_nome]
    filter_and_show_table(tabela_nome)



    #########################################
    # FORMULÁRIO PARA ADICIONAR NOVA CAPACITAÇÃO
    #########################################


    # Editar ação
    st.markdown(f"### Editar Registro em **{tabela_nome}**")
    id_editar = st.text_input(f"Digite o ID da ação a ser editada em **{tabela_nome}**:", value="")

    if st.button("Editar"):
        formulario_generico(tabela_nome, df_filtered, config_tabela['campos'], config_tabela['chave_primaria'], id_editar=id_editar)

