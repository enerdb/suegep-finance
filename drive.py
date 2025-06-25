# Módulo que faz o login no google drive usando as credenciais do arquivo credentials.json ou do arquivo .env.
# Disponibiliza a planilha do google sheets para leitura e escrita a partir de pandas DataFrame.
# Id da pasta situada no arquivo config.py
# Nome da planilha passada como argumento para a função get_sheet_from_drive.


import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import base64
import os
import pandas as pd
import json
import locale
import config

def generate_credentials():
    if not os.path.exists("credentials.json"):
        load_dotenv()
        credentials_base64 = os.getenv("GOOGLE_CREDENTIALS")
        if credentials_base64:
            credentials_json = base64.b64decode(credentials_base64).decode("utf-8")
            credentials_dict = json.loads(credentials_json)

            with open("credentials.json", "w") as f:
                f.write(json.dumps(credentials_dict))

def get_sheet_from_drive(planilha):
    generate_credentials()
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",  # Acesso a planilhas
        "https://www.googleapis.com/auth/drive",   # Acesso ao Google Drive
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(filename='credentials.json', scopes=scopes)
    client = gspread.authorize(creds)

    folder_files = client.list_spreadsheet_files(folder_id=config.ID_PASTA_GOOGLE_SHEETS)
    print([f['name'] for f in folder_files])


    id_pasta = config.ID_PASTA_GOOGLE_SHEETS
    nome_planilha = planilha
    #nome_planilha = 'BI_db'

    return client.open(title=nome_planilha, folder_id=id_pasta)


def update_worksheet_from_df(worksheet, df, debug = False):
    

    df_clean = df.copy().reset_index()

    # 1. Substitui NaN e NaT por None
    #df_clean = df.where(pd.notnull(df_clean), None) 

    # 2. Converte colunas datetime para string no formato "dd/mm/yyyy"
    for col in df_clean.select_dtypes(include=["datetime64", "datetime64[ns]"]).columns:
        if debug:
            print(df_clean[col].head())
        df_clean[col] = df_clean[col].dt.strftime("%d/%m/%Y").fillna('').infer_objects(copy=False)
        if debug:
            print(df_clean[col].head())

    # Converte colunas float para string no formato 
    for col in df_clean.select_dtypes(include=["float"]).columns:
        if debug:
            print(df_clean[col].head())
        df_clean[col] = df_clean[col].apply(lambda x: f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.').replace('nan',''))
        
        if debug:
            print(df_clean[col].head())


    # 3. Converte todos os tipos para object para evitar problemas de tipo
    df_clean = df_clean.astype(object).fillna('').infer_objects(copy=False)


    if debug:
        print("Colunas")
        print(df_clean.dtypes)
        print("DataFrame limpo:")
        print(df_clean)
    
    # 5. Atualiza a planilha com os dados do DataFrame
    worksheet.update([df_clean.columns.values.tolist()] + df_clean.values.tolist())


def get_df_from_drive(sheet, tab):
    # tab = nome da aba
    raw = sheet.worksheet(tab).get_all_values()

    # retorna dados brutos
    return pd.DataFrame(raw[1:], columns=raw[0])
    