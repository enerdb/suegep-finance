import streamlit as st

def start_filters(df_repasses):
    st.session_state['filters'] = {}
    st.session_state['filters']['fontes'] = ['FUSP']
    st.session_state['filters']['anos'] =  df_repasses['Ano_Repasse'].unique()
    st.session_state['filters']['eixos'] = df_repasses['Eixo'].unique()

def update_filters():

    fontes = st.session_state['filters']['fontes']
    anos = st.session_state['filters']['anos']
    eixos = st.session_state['filters']['eixos']

    df_repasses = st.session_state['bi_db']['Repasses']

    df_repasses_filtered = df_repasses[
        (df_repasses['Fonte'].isin(fontes)) &
        (df_repasses['Ano_Repasse'].isin(anos)) &
        (df_repasses['Eixo'].isin(eixos))
    ]

    st.session_state.filtered_db['Repasses'] = df_repasses_filtered
    st.session_state.filtered_db['Projetos'] = st.session_state['bi_db']['Projetos'][
        st.session_state['bi_db']['Projetos']['id_Repasse'].isin(df_repasses_filtered.index)
    ]
    st.session_state.filtered_db['Ações'] = st.session_state['bi_db']['Ações'][
        st.session_state['bi_db']['Ações']['id_Projeto'].isin(st.session_state.filtered_db['Projetos'].index)
    ]
    st.session_state.filtered_db['Contratações'] = st.session_state['bi_db']['Contratações'][
        st.session_state['bi_db']['Contratações']['id_Ação'].isin(st.session_state.filtered_db['Ações'].index)
    ]
    st.session_state.filtered_db['Capacitações'] = st.session_state['bi_db']['Capacitações'][
        st.session_state['bi_db']['Capacitações']['id_Ação'].isin(st.session_state.filtered_db['Ações'].index)
    ]
    st.session_state.filtered_db['Seleções'] = st.session_state['bi_db']['Seleções'][
        st.session_state['bi_db']['Seleções']['id_Capacitação'].isin(st.session_state.filtered_db['Capacitações'].index)
    ]
 
    st.session_state.filtered_db['Seleções'] = st.session_state['bi_db']['Seleções'][
        st.session_state['bi_db']['Seleções']['id_Capacitação'].isin(st.session_state.filtered_db['Capacitações'].index)
    ]

def render_sidebar():
    
    if 'bi_db' not in st.session_state:
        return # No sidebar if data is not loaded

    df_repasses = st.session_state['bi_db']['Repasses']

    if 'filters' not in st.session_state:
        start_filters(df_repasses)

    with st.sidebar:
        st.title("Filtros")
       

        st.session_state['filters']['fontes'] = st.multiselect("Selecione a fonte do repasse:", df_repasses['Fonte'].unique(), default=st.session_state['filters']['fontes'])
        st.session_state['filters']['anos'] = st.multiselect("Selecione o ano do repasse:", df_repasses['Ano_Repasse'].unique(), default=st.session_state['filters']['anos'])
        st.session_state['filters']['eixos'] = st.multiselect("Selecione o eixo do repasse:", df_repasses['Eixo'].unique(), default=st.session_state['filters']['eixos'])

        update_filters()


    # Adicione mais widgets de filtro conforme necessário