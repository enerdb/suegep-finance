
import streamlit as st
import time
import pandas as pd
import config

from sidebar import render_sidebar

from tools.format_df import formatar_df_reais



# Helper functions
    
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

#########################################
# FILTRAGEM E EXIBIÇÃO PARA EXIBIÇÃO
#########################################

# fontes = st.session_state['filters']['fontes']
# anos = st.session_state['filters']['anos']
# eixos = st.session_state['filters']['eixos']

# df_repasses_filtered = df_repasses[
#     (df_repasses['Fonte'].isin(fontes)) &
#     (df_repasses['Ano_Repasse'].isin(anos)) &
#     (df_repasses['Eixo'].isin(eixos))
# ]

df_repasses_filtered = st.session_state['filtered_db']['Repasses']

st.markdown("### Exibição de Repasses")

df_display = formatar_df_reais(df_repasses_filtered, ['Valor_Repasse_Inicial', 'Ajustes_Soma', 'Valor_Repasse_Atual'])
st.dataframe(df_display)

#########################################
# FORMULÁRIO PARA ADICIONAR NOVO REPASSE
#########################################

# FORM FUNCTIONS 

@st.dialog("Confirmação")
def confirma_escreve_repasse():
    def fecha_dialog():
        st.session_state['id_novo_repasse'] = None
        st.session_state['novo_repasse'] = None
        st.rerun()

    st.write(st.session_state['id_novo_repasse'])
    #st.write(st.session_state['novo_repasse'])

    if st.session_state['id_novo_repasse'] in st.session_state['bi_db']['Repasses'].index:
        st.warning(f"O repasse com ID `{st.session_state['id_novo_repasse']}` já existe. Deseja substituir os dados?")
    else:
        st.write("Confirma inclusão do novo repasse?")
    col1, col2 = st.columns(2)
    if col1.button("Sim"):
        df_repasses.loc[st.session_state['id_novo_repasse']] = st.session_state['novo_repasse']
        st.success("Informações de repasse incluídas com sucesso.")
        fecha_dialog()
    if col2.button("Cancelar"):
        st.warning("Operação cancelada.")
        fecha_dialog()


def formulario_adicionar_repasse():
    fonte = st.selectbox("Fonte", df_repasses['Fonte'].unique())
    ano_repasse = st.number_input("Ano do Repasse", min_value=2000, max_value=2100, value=2023)
    eixo = st.selectbox("Eixo", df_repasses['Eixo'].unique())
    natureza = st.selectbox("Natureza", df_repasses['Natureza'].unique())
    valor_repasse_inicial = st.number_input("Valor do Repasse", min_value=0.0, step=0.01)
    ajustes_soma = 0.00
    valor_repasse_atual = valor_repasse_inicial + ajustes_soma
    sei = st.text_input("Número do SEI", placeholder="Número do SEI (opcional)")
    id_repasse = f'{ano_repasse}{fonte[0]}{eixo[0]}{natureza[0]}'

    submitted = st.form_submit_button("Adicionar Repasse")

    if submitted:
        st.session_state['novo_repasse'] = {
            'Fonte': fonte,
            'Ano_Repasse': ano_repasse,
            'Eixo': eixo,
            'Natureza': natureza,
            'Valor_Repasse_Inicial': valor_repasse_inicial,
            'Ajustes_Soma': ajustes_soma,
            'Valor_Repasse_Atual': valor_repasse_atual,
            'SEI': sei
        }
        st.session_state['id_novo_repasse'] = id_repasse
        confirma_escreve_repasse()

# FORM MAIN 

st.markdown("### Adicionar Novo Repasse")
with st.expander("Formulário de Adição de Repasse"):
    with st.form("form_repasses"):
        formulario_adicionar_repasse()


#########################################
# FORMULÁRIO PARA EXCLUIR REPASSES
#########################################

st.markdown("### Excluir Repasse")
id_excluir = st.text_input("ID do Repasse a ser excluído", placeholder="Exemplo: 2023FEC")
if st.button("Excluir Repasse"):
    if id_excluir in df_repasses.index:
        df_repasses.drop(id_excluir, inplace=True)
        st.success(f"Repasse com ID `{id_excluir}` excluído com sucesso.")
        time.sleep(2)
        st.rerun()  # Recarrega a página para refletir a exclusão
    else:
        st.error(f"Repasse com ID `{id_excluir}` não encontrado.")

#########################################
# CONSULTA E ALETERAÇÃO DE HISTÓRICO DE REPASSES
#########################################
df_repasses_alteracoes = st.session_state['bi_db']['Repasses_Alterações']

st.markdown("### Consultar e Alterar Histórico de Repasse")
id_consulta = str(st.text_input("ID do Repasse para consulta", placeholder="Exemplo: 2023FEC"))
if st.button("Consultar Repasse"):
    if id_consulta in df_repasses.index:
        st.write(formatar_df_reais(df_repasses, ['Valor_Repasse_Inicial', 'Ajustes_Soma', 'Valor_Repasse_Atual']).loc[id_consulta])
        df_repasses_alteracoes_filtered = df_repasses_alteracoes[df_repasses_alteracoes['id_Repasse'] == id_consulta]
        st.write("Histórico de Alterações:")
        st.dataframe(formatar_df_reais(df_repasses_alteracoes_filtered, ['Valor_Ajuste']), 
                     column_config ={
                         'Data_Ajuste': st.column_config.DateColumn(
                             format="DD/MM/YYYY",
                             help="Valor do ajuste realizado no repasse"
                         )}
                    )
        
    else:
        st.error(f"Repasse com ID `{id_consulta}` não encontrado.")

st.markdown("###### Inserir Alteração no Repasse")
with st.expander("Formulário de Alteração de Repasse"):
    with st.form("form_alteracao_repasse"):
        evento = st.text_input("Evento de Alteração", placeholder="Descrição da alteração")
        valor_ajuste = st.number_input("Valor do Ajuste", step=0.01)
        sei_alteracao = st.text_input("Número do SEI da Alteração", placeholder="Número do SEI (opcional)")
        data_ajuste = st.date_input("Data do Ajuste", format="DD/MM/YYYY"
                                    ,value=None)

        submitted_alteracao = st.form_submit_button("Registrar Alteração")

    if submitted_alteracao:
        if id_consulta in df_repasses.index:
            nova_alteracao = {
                'id_Repasse': id_consulta,
                'Evento': evento,
                'Valor_Ajuste': valor_ajuste,
                'SEI': sei_alteracao,
                'Data_Ajuste': data_ajuste
            }
            df_repasses_alteracoes.loc[len(df_repasses_alteracoes)] = nova_alteracao
            st.session_state['bi_db']['Repasses_Alterações'] = df_repasses_alteracoes

            df_repasses_alteracoes_filtered = df_repasses_alteracoes[df_repasses_alteracoes['id_Repasse'] == id_consulta]

            alteracoes_total = df_repasses_alteracoes_filtered['Valor_Ajuste'].sum()
            st.write(f"Total de Alterações: R$ {alteracoes_total:.2f}".replace(".", ","))
            
            st.session_state['bi_db']['Repasses'].loc[id_consulta, 'Ajustes_Soma'] = alteracoes_total
            st.session_state['bi_db']['Repasses'].loc[id_consulta, 'Valor_Repasse_Atual'] = df_repasses.loc[id_consulta, 'Valor_Repasse_Inicial'] + alteracoes_total

            #st.session_state['bi_db']['Repasses']['Ajustes_Soma'].loc[id_consulta] = alteracoes_total
            #st.session_state['bi_db']['Repasses']['Valor_Repasse_Atual'].loc[id_consulta] = df_repasses.loc[id_consulta, 'Valor_Repasse_Inicial'] + alteracoes_total
            st.write(f"Valor Atualizado do Repasse: R$ {st.session_state['bi_db']['Repasses']['Valor_Repasse_Atual'].loc[id_consulta]:.2f}".replace(".", ","))
            
            update_sheets(save2sheets)
            
            
            st.success("Alteração registrada com sucesso.")

        else:
            st.error(f"Repasse com ID `{id_consulta}` não encontrado.")

