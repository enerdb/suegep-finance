import base64

# Gera as credenciais em string
with open("credentials.json", "rb") as f:
    encoded_credentials = base64.b64encode(f.read()).decode("utf-8")

# Exibir o resultado
print(encoded_credentials)