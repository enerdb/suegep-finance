import streamlit as st
import pandas as pd
from drive import get_sheet_from_drive, get_df_from_drive, update_worksheet_from_df
from read_db import read_db


if __name__ == "__main__":
    st.set_page_config(
        page_title="Importação Athena",
        page_icon=":bar_chart:",
        layout="wide")
    if 'bi_db' not in st.session_state:
        st.session_state.bi_db = read_db()
       
        # spreadsheet = get_sheet_from_drive('BI_db')
        # st.session_state.bi_db = {}
        # st.session_state.bi_db['Repasses'] = get_df_from_drive(spreadsheet, 'Repasses')
        # st.session_state.bi_db['Projetos'] = get_df_from_drive(spreadsheet, 'Projetos')
        # st.session_state.bi_db['Ações'] = get_df_from_drive(spreadsheet,'Ações')
        # st.session_state.bi_db['Contratações'] = get_df_from_drive(spreadsheet,'Contratações')
        # st.session_state.bi_db['Etapa_Contratação'] = get_df_from_drive(spreadsheet,'Etapa_Contratação')
        # st.session_state.bi_db['Capacitações'] = get_df_from_drive(spreadsheet,'Capacitações')
        # st.session_state.bi_db['Seleções'] = get_df_from_drive(spreadsheet,'Seleções')
        # st.session_state.bi_db['Inscrições'] = get_df_from_drive(spreadsheet,'Inscrições')
        # st.session_state.bi_db['Inscrições_Moodle'] = get_df_from_drive(spreadsheet,'Inscrições_Moodle')

    # Exibe os DataFrames carregados
    for key, value in st.session_state.bi_db.items():
        with st.expander(f"{key} ({value.shape[0]} linhas, {value.shape[1]} colunas)", expanded=False):
            st.write(f"**{key}**")
            st.write(value.dtypes)
            st.dataframe(value)


            spreadsheet = get_sheet_from_drive('BI_db')

    update_worksheet_from_df(spreadsheet.worksheet('Repasses'), st.session_state.bi_db['Repasses'])
    update_worksheet_from_df(spreadsheet.worksheet('Projetos'), st.session_state.bi_db['Projetos'])
    update_worksheet_from_df(spreadsheet.worksheet('Ações'), st.session_state.bi_db['Ações'], debug=True)
    update_worksheet_from_df(spreadsheet.worksheet('Contratações'), st.session_state.bi_db['Contratações'])
    update_worksheet_from_df(spreadsheet.worksheet('Etapa_Contratação'), st.session_state.bi_db['Etapa_Contratação'])
    update_worksheet_from_df(spreadsheet.worksheet('Capacitações'), st.session_state.bi_db['Capacitações'])
    update_worksheet_from_df(spreadsheet.worksheet('Seleções'), st.session_state.bi_db['Seleções'])
    update_worksheet_from_df(spreadsheet.worksheet('Inscrições'), st.session_state.bi_db['Inscrições'])
    update_worksheet_from_df(spreadsheet.worksheet('Inscrições_Moodle'), st.session_state.bi_db['Inscrições_Moodle'])


