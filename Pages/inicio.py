import streamlit as st
from drive import get_sheet_from_drive, get_df_from_drive
from read_db import read_db, print_db

from sidebar import render_sidebar


@st.cache_data
def convert_data_to_excel(data):
    """Converts a DataFrame to an Excel file in memory."""
    import pandas as pd
    from io import BytesIO

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in data.items():
            df.to_excel(writer, sheet_name=sheet_name)
            #df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)
    return output




st.title("Dados BI SUEGEP")

with st.spinner("Carregando dados do Google Sheets..."):
    if 'bi_db' not in st.session_state:
        st.session_state.bi_db = read_db()
        st.session_state.filtered_db = st.session_state.bi_db.copy()

st.success("Dados carregados com sucesso!")


st.button("Imprimir dados na tela", on_click=print_db, args=(st.session_state.bi_db, 'streamlit'))

st.download_button(
    label="Download dos dados em formato Excel",
    data=convert_data_to_excel(st.session_state.bi_db),
    file_name='dados.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

render_sidebar()

st.markdown("""
            ## Próximos passos
            - Unificar filtros no código e salvar dfs filtrados no session_state
            - Inclusão de formulários para edição dos dados.
            - Página de acompanhamento de repasses e recursos
            - Página de monitoramento de ações de projetos
            - Página para lançar ações em projetos.
            - Página de acompanhamento de ações de projetos.
            - Página de acompnhamento de contratações e execuções.
            - Página para upload de tabelas em formato csv vindas do moodle.
""")