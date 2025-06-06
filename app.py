import streamlit as st
from drive import get_sheet_from_drive, get_df_from_drive


def main():
    st.title("Google Sheets Viewer")
    st.write("Welcome to the Google Sheets Viewer!")
    st.write("Please select a sheet from the dropdown below:")

    spreadsheet = get_sheet_from_drive('BI_db')
    
    st.write('Planilha coletada')

    st.write(get_df_from_drive(spreadsheet, 'Repasses'))

    st.write(get_df_from_drive(spreadsheet, 'Projetos'))


if __name__ == "__main__":
    main()
