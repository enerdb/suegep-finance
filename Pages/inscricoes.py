import streamlit as st
import time
import pandas as pd
import config


if 'bi_db' not in st.session_state:
    st.error("Dados não carregados. Por favor, volte para a página inicial e carregue os dados.")
    st.stop()


st.title("Inscrições")
st.markdown("### Carregue aqui os arquivos de inscrições gerados pelo Ozéias")

novo_csv = st.file_uploader("Upload do arquivo de inscrições", type=["csv"], key="file_uploader_inscricoes")
if novo_csv is not None:
    try:
        df_novo_csv = pd.read_csv(novo_csv)
        
        st.error("Ozeias ainda não passou o layout final do arquivo de inscrições. Nada será feito com esse arquivo por enquanto.")
         # Placeholder for future processing logic
         
         # Example: Display the uploaded DataFrame
         #

        #st.success("Arquivo carregado com sucesso!")
        st.dataframe(df_novo_csv)
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")


#########################################
# Exibição de inscrições de uma ação
#########################################

st.markdown("### Exibição de inscrições de uma capacitação específica")
id_capacitacao = st.text_input("ID da Capacitação")

col1, col2 = st.columns(2)

exibir_inscricoes = col1.button("Exibir inscrições resumidas")
exibir_detalhadas = col2.button("Exibir inscrições detalhadas")

if exibir_inscricoes or exibir_detalhadas:
    if not id_capacitacao:
        st.error("Por favor, insira um ID de Capacitação válido.")
        st.stop()
    elif exibir_inscricoes:
        df_inscricoes = st.session_state['bi_db']['Inscrições']
        df_inscricoes_filtered = df_inscricoes[df_inscricoes['id_Capacitação'] == id_capacitacao]
    elif exibir_detalhadas:
        df_inscricoes = st.session_state['bi_db']['Inscrições_Moodle']
        df_inscricoes_filtered = df_inscricoes[df_inscricoes['id_Capacitação'] == id_capacitacao]
    st.dataframe(df_inscricoes_filtered)




    