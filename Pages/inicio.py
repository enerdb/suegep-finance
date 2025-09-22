import streamlit as st
from drive import get_sheet_from_drive, get_df_from_drive
from read_db import print_db, read_db_excel, read_db_drive, update_db_drive

from sidebar import render_sidebar


##############################
# Funções auxiliares
##############################

@st.cache_data
def convert_data_to_excel(data):
    """Converts a DataFrame to an Excel file in memory."""
    import pandas as pd
    from io import BytesIO

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in data.items():

            # Só exporta índice se ele não for o RangeIndex padrão (0,1,2,...)
            export_index = not isinstance(df.index, pd.RangeIndex)
            df.to_excel(writer, sheet_name=sheet_name, index=export_index)
            
    output.seek(0)
    return output

def convert_excel_to_data(file):
    import pandas as pd

    # lê todas as planilhas de uma vez (retorna dict {sheet_name: df})
    data = pd.read_excel(file, sheet_name=None)
    
    return data




###############################
# Main
###############################

st.title("Dados BI SUEGEP")

################################
# Carga dos dados do drive

with st.spinner("Carregando dados do Google Sheets..."):
    if 'bi_db' not in st.session_state:
        st.session_state.bi_db = read_db_drive()
        st.session_state.filtered_db = st.session_state.bi_db.copy()

st.success("Dados carregados com sucesso!")

################################
# Imprimir dados na tela

st.button("Imprimir dados na tela", on_click=print_db, args=(st.session_state.bi_db, 'streamlit'))

################################
# Download dos dados em Excel

st.download_button(
    label="Download dos dados em formato Excel (serve como backup)",
    data=convert_data_to_excel(st.session_state.bi_db),
    file_name='dados.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

################################
# Salva dados no drive

if st.button("Atualizar dados para o drive"):
    with st.spinner("Carregando dados para o Google Sheets..."):
        update_db_drive(st.session_state.bi_db)
    st.success("Dados atualizados com sucesso!")

################################
# Upload de dados em Excel do backup

st.markdown("##### Restaurar dados a partir do último download em formato Excel")

uploaded_file = st.file_uploader("Selecione um arquivo Excel", type=["xlsx"])
if uploaded_file is not None:
    data_dict = read_db_excel(uploaded_file)
    if data_dict.keys() != st.session_state.bi_db.keys():
        st.error("O arquivo Excel enviado não contém as abas esperadas.")
        st.stop()
    
    st.session_state.bi_db = data_dict
    st.session_state.filtered_db = st.session_state.bi_db.copy()


################################
# Sidebar

render_sidebar()

################################
# Rascunho de próximos passos


st.markdown("""
            #### Próximos passos
            - Unificar filtros no código e salvar dfs filtrados no session_state
            - Inclusão de formulários para edição dos dados.
            - Página de acompanhamento de repasses e recursos
            - Página de monitoramento de ações de projetos
            - Página para lançar ações em projetos.
            - Página de acompanhamento de ações de projetos.
            - Página de acompnhamento de contratações e execuções.
            - Página para upload de tabelas em formato csv vindas do moodle.
""")