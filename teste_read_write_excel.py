import streamlit as st
import pandas as pd
from office365_utils import get_df_from_excel, update_excel_from_df, autenticar
from drive import get_sheet_from_drive, get_df_from_drive, update_worksheet_from_df

from read_db import read_db

if __name__ == "__main__":
    st.set_page_config(
        page_title="Importação Google Sheets",
        page_icon=":bar_chart:",
        layout="wide")
    
    if 'bi_db' not in st.session_state:
        st.session_state.bi_db = read_db()
        
        # # Lê o arquivo Excel do OneDrive/SharePoint
        # st.session_state.bi_db['Repasses'] = get_df_from_excel("/Documentos Compartilhados/Repasses.xlsx")
        # st.session_state.bi_db['Projetos'] = get_df_from_excel("/Documentos Compartilhados/Projetos.xlsx")
        # st.session_state.bi_db['Ações'] = get_df_from_excel("/Documentos Compartilhados/Ações.xlsx")
        # st.session_state.bi_db['Contratações'] = get_df_from_excel("/Documentos Compartilhados/Contratações.xlsx")
        # st.session_state.bi_db['Etapa_Contratação'] = get_df_from_excel("/Documentos Compartilhados/Etapa_Contratação.xlsx")
        # st.session_state.bi_db['Capacitações'] = get_df_from_excel("/Documentos Compartilhados/Capacitações.xlsx")
        # st.session_state.bi_db['Seleções'] = get_df_from_excel("/Documentos Compartilhados/Seleções.xlsx")
        # st.session_state.bi_db['Inscrições'] = get_df_from_excel("/Documentos Compartilhados/Inscrições.xlsx")
        # st.session_state.bi_db['Inscrições_Moodle'] = get_df_from_excel("/Documentos Compartilhados/Inscrições_Moodle.xlsx")

    for key, value in st.session_state.bi_db.items():
        with st.expander(f"{key} ({value.shape[0]} linhas, {value.shape[1]} colunas)", expanded=False):
            st.write(f"**{key}**")
            st.write(value.dtypes)
            st.dataframe(value)

    ctx = autenticar()
    # Atualiza os arquivos Excel no OneDrive/SharePoint
    file = "/Documentos Compartilhados/dados.xlsx"
    abas= ['Repasses', 'Projetos', 'Ações', 'Contratações', 'Etapa_Contratação', 'Capacitações', 'Seleções', 'Inscrições', 'Inscrições_Moodle']

    for aba in abas:
        update_excel_from_df(st.session_state.bi_db[aba], ctx, file, aba)

    