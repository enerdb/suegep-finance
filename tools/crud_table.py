import streamlit as st
import time
import pandas as pd
from tools.format_df import formatar_df_datas, formatar_df_reais

##########################################
# Helper functions
def get_new_id(df, chave_primaria, novo_registro):
    if chave_primaria == 'id_Contratação' or chave_primaria == 'id_Capacitação':

        # filtrar a ação correspondente à contratação e obter o projeto e o repasse
        id_acao = novo_registro['id_Ação']
        if id_acao not in st.session_state['bi_db']['Ações'].index.astype(str):
            st.error(f"Ação `{id_acao}` não encontrada. Verifique o ID na tabela de Ações.")
            st.stop()

        id_projeto = st.session_state['bi_db']['Ações'].loc[id_acao, 'id_Projeto']
        if id_projeto not in st.session_state['bi_db']['Projetos'].index.astype(str):
            st.error(f"Projeto `{id_projeto}` não encontrado. Verifique o ID na tabela de Projetos.")
            st.stop()

        id_repasse = st.session_state['bi_db']['Projetos'].loc[id_projeto, 'id_Repasse']
        if id_repasse not in st.session_state['bi_db']['Repasses'].index.astype(str):
            st.error(f"Repasse `{id_repasse}` não encontrado. Verifique o ID na tabela de Repasses.")
            st.stop()

        return f"{id_repasse}-{int(id_projeto):03d}-{int(id_acao):04d}"

    else:
        return int(df.index.astype(int).max() + 1) if not df.empty else 1



def exibir_tabela(df, cols_datas=None, cols_monetarios = None):
    df_display = df
    if cols_datas:
        df_display = formatar_df_datas(df_display, cols_datas)
    if cols_monetarios:
        df_display = formatar_df_reais(df_display, cols_monetarios)

    st.dataframe(df_display)


def formulario_generico(tabela_nome, df, campos, chave_primaria):
    st.markdown(f"### Adicionar Novo Registro em **{tabela_nome}**")

    with st.expander("Formulário de Adição"):
        with st.form(f"form_novo_{tabela_nome}"):
            novo_registro = {}

            for campo, tipo, origem in campos:
                if tipo == 'text':
                    novo_registro[campo] = st.text_input(campo)

                elif tipo == 'selectbox':
                    if isinstance(origem, list):
                        opcoes = origem

                    elif isinstance(origem, str):    
                    # Busca opções de outra tabela
                        if origem in st.session_state['bi_db']:
                            df_ref = st.session_state['bi_db'][origem]

                            if campo == df_ref.index.name:
                                opcoes = df_ref.index.tolist()
                            else:
                                opcoes = df_ref[campo].dropna().unique().tolist()
                        else:
                            opcoes = []
                    novo_registro[campo] = st.selectbox(campo, opcoes)
                             
                elif tipo == 'date':
                    novo_registro[campo] = st.date_input(campo, format="DD/MM/YYYY", value=None)
                elif tipo == 'number':
                    novo_registro[campo] = st.number_input(campo)

            id_novo = get_new_id(df, chave_primaria, novo_registro) 

            submitted = st.form_submit_button("Adicionar")
            if submitted:
                st.session_state['novo_registro'] = novo_registro
                st.session_state['id_novo'] = id_novo
                confirma_escrita(tabela_nome, df, chave_primaria)


def confirma_escrita(tabela_nome, df, chave_primaria):
    @st.dialog("Confirmação")
    def _dialog():
        id_novo = st.session_state['id_novo']
        novo = st.session_state['novo_registro']
        st.write(f"Confirma inclusão de novo registro em **{tabela_nome}**?")
        st.write(novo)
        col1, col2 = st.columns(2)
        if col1.button("Sim"):
            df.loc[id_novo] = novo
            st.success(f"Registro incluído em **{tabela_nome}** com sucesso.")
            time.sleep(1)
            st.rerun()
        if col2.button("Cancelar"):
            st.warning("Operação cancelada.")
            st.session_state.pop('novo_registro', None)
            st.session_state.pop('id_novo', None)

    _dialog()


def formulario_exclusao(tabela_nome, df):
    st.markdown(f"### Excluir Registro de **{tabela_nome}**")
    id_excluir = st.text_input("ID a ser excluído", placeholder="Verificar na tabela acima")
    if st.button("Excluir"):
        if id_excluir in df.index.astype(str):
            df.drop(id_excluir, inplace=True)
            st.success(f"Registro `{id_excluir}` excluído de **{tabela_nome}** com sucesso.")
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"ID `{id_excluir}` não encontrado em **{tabela_nome}**.")
