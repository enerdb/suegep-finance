import streamlit as st
import pandas as pd
import time


def excluir_item(id_excluir, df_to_modify, tipo_item="Item"):
    if id_excluir in df_to_modify.index:
        df_to_modify.drop(id_excluir, inplace=True)
        st.success(f"{tipo_item} com ID `{id_excluir}` excluída com sucesso.")
        time.sleep(2)
        st.rerun()  # Recarrega a página para refletir a exclusão
    else:
        st.error(f"{tipo_item} com ID `{id_excluir}` não encontrado(a).")