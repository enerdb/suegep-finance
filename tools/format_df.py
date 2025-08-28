import pandas as pd

def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_df_reais(df, colunas):
    df1 = df.copy()
    for col in colunas:
        if col in df1.columns and pd.api.types.is_numeric_dtype(df1[col]):
            df1[col] = df1[col].apply(formatar_reais)
    return df1


def formatar_df_datas(df, colunas):
    df1 = df.copy()
    for col in colunas:
        if col in df1.columns and pd.api.types.is_datetime64_any_dtype(df1[col]):
            df1[col] = df1[col].dt.strftime('%d/%m/%Y')
    return df1