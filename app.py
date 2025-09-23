import streamlit as st


########################################
# LAYOUT CONFIG
########################################

st.set_page_config(layout = 'wide')



def main():

    pages = {
    "Geral": [
        st.Page("Pages/inicio.py",                title="Início"),
    ],
    "Financeiro": [
        st.Page("Pages/repasses.py",            title="Repasses"),
        st.Page("Pages/projetos.py",            title="Projetos"),
        st.Page("Pages/acoes.py",               title="Ações"),
        st.Page("Pages/contratacoes.py",        title="Contratações"),
    ],
    "Ensino": [
        st.Page("Pages/capacitacoes.py",        title="Capacitações"),
        st.Page("Pages/selecoes.py",            title="Seleções"),
        st.Page("Pages/inscricoes.py",          title="Carregar Inscrições"),
    ],
    "Programas": [
        st.Page("Pages/metas.py",               title="Metas"),
    ]

    
    # "Cadastrar ou Alterar": [
    #     st.Page("paginas/cadastro_novo_servidor.py",title="Novo Servidor"),
    #     st.Page("paginas/cadastro_alterar_servidor.py",     title="Alterar dados servidor"),
    #     st.Page("paginas/cadastro_abono.py",        title="Abono anual"),
    #     st.Page("paginas/cadastros_google.py",      title="Outros cadastros"),
    # ],
}
    pg = st.navigation(pages)
    pg.run()




###########################
# Pages Config
###########################


if __name__ == "__main__":
    main()



########################################
# COMMANDS
########################################
# Set-ExecutionPolicy Unrestricted -Scope Process
# venv\Scripts\Activate.ps1
# streamlit run app.py