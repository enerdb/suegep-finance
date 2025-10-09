ID_PASTA_GOOGLE_SHEETS = '1U71AJACDebDEQ06lG7jgHCaOi25xBuVY'

SAVE2SHEETS = True

TABELAS_CONFIG  = {
    'Repasses': {
        'chave_primaria': 'id_Repasses',
        'campos': [
            ('Ano_Repasse', 'selectbox', 'Repasses'),  # Options to be filled dynamically
            ('Fonte', 'selectbox', 'Repasses'),  # Options to be filled dynamically
            ('Eixo', 'selectbox', 'Repasses'),  # Options to be filled dynamically
            ('Natureza', 'selectbox', 'Repasses'),  # Options to be filled dynamically
            ('Valor_Repasse_Inicial', 'number', None),
            ('Ajustes_Soma', 'number', None),
            ('Valor_Repasse_Atual', 'number', None),
            ('SEI', 'text', None),
        ],
        'cols_datas': [],
        'cols_monetarios': ['Valor_Repasse_Inicial', 'Ajustes_Soma', 'Valor_Repasse_Atual'],
    },
    'Projetos': {
        'chave_primaria': 'id_Projeto',
        'campos': [
            ('Nome_Projeto', 'text', None),
            ('id_Repasse', 'selectbox', 'Repasses'),  # Options to be filled dynamically
            ('Valor_Planejado_Inicial', 'number', None),
            ('Ajustes_Soma', 'number', None),
            ('Valor_Planejado_Atual', 'number', None)
        ],
        'cols_datas': [],
        'cols_monetarios': ['Valor_Planejado_Inicial', 'Ajustes_Soma', 'Valor_Planejado_Atual'],
    },
    'Ações': {
        'chave_primaria': 'id_Ação',
        'campos': [
            ('Nome_Ação', 'text', None),
            ('id_Projeto', 'selectbox', 'Projetos'), 
            ('Data_Início_Planejado', 'date', None),
            ('Data_Fim_Planejado', 'date', None),
            ('Data_Início_Real', 'date', None),
            ('Data_Fim_Real', 'date', None),
            ('Status', 'text', None),
            ('Histórico', 'text', None),
        ],
        'cols_datas': ['Data_Início_Planejado', 'Data_Fim_Planejado', 'Data_Início_Real', 'Data_Fim_Real'],
        'cols_monetarios': [],
    },
    'Contratações': {
        'chave_primaria': 'id_Contratação',
        'campos': [
            ('id_Ação', 'selectbox', 'Ações'),  # Options to be filled dynamically
            ('CNPJ_Contratada', 'text', None),
            ('Nome_Contratada', 'text', None),
            ('Data_Contrato', 'date', None),
            ('Data_Encerramento_Contrato', 'date', None),
            ('Valor_Reservado', 'number', None),
            ('Valor_Empenhado', 'number', None),
            ('Valor_Liquidado', 'number', None),
            ('Etapa_Atual', 'selectbox', ['Planejamento', 'Contratação', 'Execução', 'Contrato Encerrado'])
        ],
        'cols_datas': ['Data_Contrato', 'Data_Encerramento_Contrato'],
        'cols_monetarios': ['Valor_Reservado', 'Valor_Empenhado', 'Valor_Liquidado'],
    },
# Faltam outras tabelas


}
