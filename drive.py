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


def update_worksheet_from_df(worksheet, df):
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())


def get_df_from_drive(sheet, tab):
    # tab = nome da aba
    return pd.DataFrame(sheet.worksheet(tab).get_all_records())