
import streamlit as st
import time
import pandas as pd
import config

from sidebar import render_sidebar


from tools.format_df import formatar_df_reais

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

save2sheets = config.SAVE2SHEETS

render_sidebar()

df_repasses = st.session_state['bi_db']['Repasses']
df_projetos = st.session_state['bi_db']['Projetos']

#########################################
# FILTRAGEM E EXIBIÇÃO PARA EXIBIÇÃO
#########################################

df_repasses_filtered = st.session_state['filtered_db']['Repasses']
df_projetos_filtered = st.session_state['filtered_db']['Projetos']

st.markdown("### Exibição de Projetos")

df_display = formatar_df_reais(df_projetos_filtered, ['Valor_Planejado_Inicial', 'Ajustes_Soma', 'Valor_Planejado_Atual'])
st.dataframe(df_display)

#########################################
# FORMULÁRIO PARA ADICIONAR NOVO PROJETO
#########################################

# FORM FUNCTIONS 

@st.dialog("Confirmação")
def confirma_escreve_projeto():
    def fecha_dialog():
        st.session_state['id_novo_projeto'] = None
        st.session_state['novo_projeto'] = None
        st.rerun()

    st.write(f"Projeto {st.session_state['id_novo_projeto']} - {st.session_state['novo_projeto']['Nome_Projeto']}")
    st.write(f"no repasse {st.session_state['novo_projeto']['id_Repasse']}")


    if st.session_state['id_novo_projeto'] in st.session_state['bi_db']['Projetos'].index:
        st.warning(f"O projeto com ID `{st.session_state['id_novo_projeto']}` já existe. Deseja substituir os dados?")
    else:
        st.write("Confirma inclusão do novo projeto?")
    col1, col2 = st.columns(2)
    if col1.button("Sim"):
        df_projetos.loc[st.session_state['id_novo_projeto']] = st.session_state['novo_projeto']
        
        st.write(f"id do novo projeto: {st.session_state['id_novo_projeto']}")
        
        st.write(df_projetos.loc[st.session_state['id_novo_projeto']])
        
        # st.write(st.session_state['novo_projeto'])


        #st.session_state['bi_db']['Repasses'].loc[id_consulta, 'Ajustes_Soma'] = alteracoes_total


        if (False):
            st.error("Erro ao incluir o projeto. Verifique os dados e tente novamente.")
        else:
            st.success("Informações de projeto incluídas com sucesso.")
        time.sleep(10)
        fecha_dialog()
    if col2.button("Cancelar"):
        st.warning("Operação cancelada.")
        fecha_dialog()


def formulario_adicionar_projeto():

    id_Repasse = st.selectbox("ID do Repasse (Ano + Fonte + Inicial do eixo + Inicial Custeio ou Investimento)", df_repasses.index)
    nome_projeto = st.text_input("Nome do Projeto", placeholder="Nome do Projeto")
    valor_planejado_inicial = st.number_input("Valor Planejado Inicial (R$)", min_value=0.0, step=0.01)
    ajustes_soma = 0.00
    valor_planejado_atual = valor_planejado_inicial + ajustes_soma
    id_projeto = df_projetos.index.astype(int).max() + 1

    submitted = st.form_submit_button("Adicionar Projeto")

    if submitted:
        st.session_state['novo_projeto'] = {
            'id_Repasse': id_Repasse,
            'Nome_Projeto': nome_projeto,
            'Valor_Planejado_Inicial': valor_planejado_inicial,
            'Ajustes_Soma': ajustes_soma,
            'Valor_Planejado_Atual': valor_planejado_atual
        }
        st.session_state['id_novo_projeto'] = id_projeto
        confirma_escreve_projeto()

# FORM MAIN 

st.markdown("### Adicionar Novo Projeto")
with st.expander("Formulário de Adição de Projeto"):
    with st.form("form_novo_projeto"):
        formulario_adicionar_projeto()


#########################################
# FORMULÁRIO PARA EXCLUIR PROJETOS
#########################################

st.markdown("### Excluir Projeto")
id_excluir = st.text_input("ID do Projeto a ser excluído", placeholder="Verificar na tabela acima")
if st.button("Excluir Projeto"):
    if id_excluir in df_projetos.index:
        df_projetos.drop(id_excluir, inplace=True)
        st.success(f"Projeto com ID `{id_excluir}` excluído com sucesso.")
        time.sleep(2)
        st.rerun()  # Recarrega a página para refletir a exclusão
    else:
        st.error(f"Projeto com ID `{id_excluir}` não encontrado.")


#########################################
# CONSULTA E ALETERAÇÃO DE HISTÓRICO DE PROJETOS
#########################################
df_projetos_alteracoes = st.session_state['bi_db']['Projetos_Alterações']


st.markdown("### Consultar e Alterar Histórico de Projetos")
id_consulta = str(st.text_input("ID do Projeto para consulta", placeholder="Consultar na tabela acima"))

# Manter enquanto o id estiver sequencial
 
if st.button("Consultar Projeto"):

    if id_consulta in df_projetos.index:
        st.write(formatar_df_reais(df_projetos, ['Valor_Planejado_Inicial', 'Ajustes_Soma', 'Valor_Planejado_Atual']).loc[id_consulta])
        df_projetos_alteracoes_filtered = df_projetos_alteracoes[df_projetos_alteracoes['id_Projeto'] == id_consulta]
        st.write("Histórico de Alterações:")
        st.dataframe(formatar_df_reais(df_projetos_alteracoes_filtered, ['Valor_Ajuste']), 
                     column_config ={
                         'Data_Ajuste': st.column_config.DateColumn(
                             format="DD/MM/YYYY",
                             help="Valor do ajuste realizado no projeto"
                         )}
                    )
        
    else:
        st.error(f"Projeto com ID `{id_consulta}` não encontrado.")

st.markdown("###### Inserir Alteração no Projeto")
with st.expander("Formulário de Alteração de Projeto"):
    with st.form("form_alteracao_projeto"):
        evento = st.text_input("Evento de Alteração", placeholder="Descrição da alteração")
        valor_ajuste = st.number_input("Valor do Ajuste", step=0.01)
        sei_alteracao = st.text_input("Número do SEI da Alteração", placeholder="Número do SEI (opcional)")
        data_ajuste = st.date_input("Data do Ajuste", format="DD/MM/YYYY"
                                    ,value=None)

        submitted_alteracao = st.form_submit_button("Registrar Alteração")

    if submitted_alteracao:
        if id_consulta in df_projetos.index:
            nova_alteracao = {
                'id_Projeto': id_consulta,
                'Evento': evento,
                'Valor_Ajuste': valor_ajuste,
                'SEI': sei_alteracao,
                'Data_Ajuste': data_ajuste
            }
            df_projetos_alteracoes.loc[len(df_projetos_alteracoes)] = nova_alteracao
            st.session_state['bi_db']['Projetos_Alterações'] = df_projetos_alteracoes

            df_projetos_alteracoes_filtered = df_projetos_alteracoes[df_projetos_alteracoes['id_Projeto'] == id_consulta]

            alteracoes_total = df_projetos_alteracoes_filtered['Valor_Ajuste'].sum()
            st.write(f"Total de Alterações: R$ {alteracoes_total:.2f}".replace(".", ","))
            
            st.session_state['bi_db']['Projetos'].loc[id_consulta, 'Ajustes_Soma'] = alteracoes_total
            st.session_state['bi_db']['Projetos'].loc[id_consulta, 'Valor_Planejado_Atual'] = df_projetos.loc[id_consulta, 'Valor_Planejado_Inicial'] + alteracoes_total

            
            st.write(f"Valor Atualizado do Projeto: R$ {st.session_state['bi_db']['Projetos']['Valor_Planejado_Atual'].loc[id_consulta]:.2f}".replace(".", ","))
            
            update_sheets(save2sheets)
            
            
            st.success("Alteração registrada com sucesso.")

        else:
            st.error(f"Projeto com ID `{id_consulta}` não encontrado.")

