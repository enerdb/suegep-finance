from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv

# Configurações do site SharePoint/OneDrive (ajuste para sua empresa)
# site_url = "https://suaempresa.sharepoint.com/sites/nomedosite"  # ou use seu OneDrive root

def autenticar():
    from dotenv import load_dotenv
    import os

    load_dotenv()
    global MS_USERNAME, MS_PW, MS_FILE_PATH, SITE_URL
    username = os.getenv("MS_USERNAME")
    senha = os.getenv("MS_PW")
    #arquivo_excel = os.getenv("MS_FILE_PATH")
    site_url = os.getenv("SITE_URL")  # ou use seu OneDrive root

    ctx_auth = AuthenticationContext(site_url)
    if not ctx_auth.acquire_token_for_user(username, senha):
        raise Exception("Erro ao autenticar. Verifique suas credenciais.")
        
    ctx = ClientContext(site_url, ctx_auth)
    return ctx



def get_df_from_excel(arquivo_excel):
    """Lê um arquivo Excel do OneDrive/SharePoint e retorna um DataFrame do Pandas.
    Args:
        arquivo_excel (str): Caminho do arquivo Excel no OneDrive/SharePoint. Ex: "/Documentos Compartilhados/dados.xlsx"
    Returns: 
        pd.DataFrame: DataFrame contendo os dados do Excel.
    """

    # Autentica e obtém o arquivo Excel do OneDrive/SharePoint
    ctx = autenticar()
    response = File.open_binary(ctx, arquivo_excel)

    # Lê o conteúdo do Excel em um DataFrame
    bytes_file_obj = BytesIO()
    bytes_file_obj.write(response.content)
    bytes_file_obj.seek(0)
    return pd.read_excel(bytes_file_obj)


### Editar ou sobrescrever dados

def update_excel_from_df(df, ctx, arquivo_excel, sheet_name):

    # Salvar de volta no OneDrive
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Escreve o DataFrame no Excel
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    output.seek(0)

    File.save_binary(ctx, server_relative_url=arquivo_excel, content=output)
    ctx.execute_query()


    # Envia o arquivo atualizado para o OneDrive/SharePoint
    # target_file = ctx.web.get_file_by_server_relative_url(arquivo_excel)
    # target_file.save_binary(output)
    # ctx.execute_query()




    #target_file = ctx.web.get_file_by_server_relative_url(arquivo_excel)
    #target_file.upload_content(output.read())
    #ctx.execute_query()


# ✅ Conectar o Excel ao Power BI 360
# Salve o Excel em uma biblioteca de documentos do SharePoint ou OneDrive for Business.

# No Power BI Desktop:

# Use "Obter dados > SharePoint Folder" ou "Excel Online (Business)".

# Selecione o arquivo e a tabela ou aba.

# Publique para o Power BI Service.

# Configure atualização agendada, que funcionará porque está em OneDrive/SharePoint corporativo.

# 🧩 Conclusão
# ✅ Você pode sincronizar dados do seu app Python com o Power BI 360 sem pagar nada usando:

# Office365-REST-Python-Client para salvar o Excel no OneDrive

# Power BI Service lendo esse Excel diretamente

# Atualizações automáticas no Power BI Service, sem Power Automate


def get_sheet_from_drive(planilha):
    pass
def update_worksheet_from_df(worksheet, df, debug = False):
    pass

def get_df_from_drive(sheet, tab):
    pass

def generate_credentials():
    pass
