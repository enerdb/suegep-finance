
import streamlit as st
import time
import pandas as pd
import config

from sidebar import render_sidebar

from tools.format_df import formatar_df_datas

#########################################
# Helper functions
##########################################
# PRECISA CRIAR UM MÓDULO PARA ISSO

   
def update_sheets(save2sheets):
    if save2sheets:
        # Implement the logic to save df to Google Sheets
        pass  # Placeholder for actual implementation

#########################################
# CARGA DE DADOS
#########################################

if 'bi_db' not in st.session_state:
    st.error("Dados não carregados. Por favor, volte para a página inicial e carregue os dados.")
    st.stop()

render_sidebar()

save2sheets = config.SAVE2SHEETS

df_repasses = st.session_state['bi_db']['Repasses']
df_projetos = st.session_state['bi_db']['Projetos']
df_acoes = st.session_state['bi_db']['Ações']

#########################################
# FILTRAGEM E EXIBIÇÃO PARA EXIBIÇÃO
#########################################


df_repasses_filtered = st.session_state['filtered_db']['Repasses']
df_projetos_filtered = st.session_state['filtered_db']['Projetos']
df_acoes_filtered = st.session_state['filtered_db']['Ações']


st.markdown("### Exibição de Ações")

cols_datas = ['Data_Início_Planejado', 'Data_Fim_Planejado', 'Data_Início_Real', 'Data_Fim_Real']


df_display = formatar_df_datas(df_acoes_filtered, cols_datas)
st.dataframe(df_display)

#########################################
# FORMULÁRIO PARA ADICIONAR NOVO AÇÃO
#########################################

# FORM FUNCTIONS 

@st.dialog("Confirmação")
def confirma_escreve_acao():
    def fecha_dialog():
        st.session_state['id_nova_acao'] = None
        st.session_state['nova_acao'] = None
        st.rerun()

    st.write(f"Ação {st.session_state['id_nova_acao']} - {st.session_state['id_nova_acao']['Nome_Ação']}")
    st.write(f"no projeto {st.session_state['nova_acao']['id_Projeto']}")


    if st.session_state['id_nova_acao'] in st.session_state['bi_db']['Ações'].index:
        st.warning(f"Ação  com ID `{st.session_state['id_nova_acao']}` já existe. Deseja substituir os dados?")
    else:
        st.write("Confirma inclusão da nova ação?")
    col1, col2 = st.columns(2)
    if col1.button("Sim"):
        df_acoes.loc[st.session_state['id_nova_acao']] = st.session_state['nova_acao']
        
        st.write(f"id da nova ação: {st.session_state['id_novo_projeto']}")
        
        st.write(df_projetos.loc[st.session_state['id_nova_acao']])
        

        if (False):
            st.error("Erro ao incluir o ação. Verifique os dados e tente novamente.")
        else:
            st.success("Informações da ação incluídas com sucesso.")
        time.sleep(10)
        fecha_dialog()
    if col2.button("Cancelar"):
        st.warning("Operação cancelada.")
        fecha_dialog()


def formulario_adicionar_acao():

    id_Projeto = st.selectbox("ID do Projeto)", df_projetos.index)
    nome_acao = st.text_input("Nome da Ação", placeholder="Nome da Ação")

    tipo_acao = st.selectbox("Tipo de Ação", ["Capacitação", "Valorização", "Outros"])
    data_inicio_planejado = st.date_input("Data Início Planejado", format="DD/MM/YYYY", value=None)
    data_fim_planejado = st.date_input("Data Fim Planejado", format="DD/MM/YYYY", value=None)
    data_inicio_real = st.date_input("Data Início Real", format="DD/MM/YYYY", value=None)
    data_fim_real = st.date_input("Data Fim Real", format="DD/MM/YYYY", value=None)
    status = st.text_input("Status da Ação")
    historico = st.text_input("Histórico da Ação")

    id_acao = df_acoes.index.astype(int).max() + 1

    submitted = st.form_submit_button("Adicionar Ação")

    if submitted:
        st.session_state['nova_acao'] = {
            'id_Projeto': id_Projeto,
            'Nome_Ação': nome_acao,
            'Tipo_Ação': tipo_acao,
            'Data_Início_Planejado': data_inicio_planejado,
            'Data_Fim_Planejado': data_fim_planejado,
            'Data_Início_Real': data_inicio_real,
            'Data_Fim_Real': data_fim_real,
            'Status': status,
            'Histórico': historico
        }
         
        st.session_state['id_nova_acao'] = id_acao
        confirma_escreve_acao()

# FORM MAIN 

st.markdown("### Adicionar Nova Ação")
with st.expander("Formulário de Adição de Ação"):
    with st.form("form_nova_acao"):
        formulario_adicionar_acao()


#########################################
# FORMULÁRIO PARA EXCLUIR AÇÕES
#########################################

st.markdown("### Excluir Ação")
id_excluir = st.text_input("ID da Ação a ser excluída", placeholder="Verificar na tabela acima")
if st.button("Excluir Ação"):
    if id_excluir in df_acoes.index:
        df_acoes.drop(id_excluir, inplace=True)
        st.success(f"Ação com ID `{id_excluir}` excluída com sucesso.")
        time.sleep(2)
        st.rerun()  # Recarrega a página para refletir a exclusão
    else:
        st.error(f"Ação com ID `{id_excluir}` não encontrada.")



