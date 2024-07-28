import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px
# import plotly.graph_objects as go
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import yaml
from yaml.loader import SafeLoader


st.set_page_config(
    page_title="Consumo Elétrico - GEDAE",
    # layout="wide",
    initial_sidebar_state="auto",
    page_icon="📊",
    # page_icon="logoGEDAE.png",
)

@st.cache_data
def load_data(pasta):
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    df['Data'] = pd.to_datetime(df['Data'])
    df.set_index('Data', inplace=True)
    return df


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    st.secrets["cookies"]['name'],
    st.secrets["cookies"]["key"]
)

nome, status_login, user = authenticator.login()

if status_login == False:
    st.error("Usuário/Senha incorreto")
if status_login == None:
    st.warning("Digite seu login e senha")
if status_login:
    authenticator.logout('Logout', 'sidebar')

    # Credenciais da api do google
    creds_json = {
    "type": st.secrets["google_sheets"]["type"],
    "project_id": st.secrets["google_sheets"]["project_id"],
    "private_key_id": st.secrets["google_sheets"]["private_key_id"],
    "private_key": st.secrets["google_sheets"]["private_key"].replace('\\n', '\n'),
    "client_email": st.secrets["google_sheets"]["client_email"],
    "client_id": st.secrets["google_sheets"]["client_id"],
    "auth_uri": st.secrets["google_sheets"]["auth_uri"],
    "token_uri": st.secrets["google_sheets"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["google_sheets"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["google_sheets"]["client_x509_cert_url"]
}
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
    client = gspread.authorize(creds)
    sheet_name = "Dados"
    dados = load_data(sheet_name)

    meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    # Obter os meses e anos únicos dos dados
    meses_disponiveis = sorted(dados.index.month.unique())
    anos_disponiveis = sorted(dados.index.year.unique())

    # Sidebar para selecionar o mês e ano
    st.sidebar.title("Navegação")
    mes_selecionado = st.sidebar.selectbox(
        "Selecione o mês", meses_disponiveis, format_func=lambda x: meses[x - 1]
    )
    ano_selecionado = st.sidebar.selectbox("Selecione o ano", anos_disponiveis)

    # Título do Dashboard
    st.title(
        f"Tarifa por consumo elétrico - {meses[mes_selecionado-1]} {ano_selecionado}"
    )

    # Filtrar dados para o mês e ano selecionados
    dados_filtrados = dados[
        (dados.index.month == mes_selecionado) & (dados.index.year == ano_selecionado)
    ]

    dias_com_dados_por_casa = {}
    consumo_medio_mensal_dict = {}

    for coluna in dados_filtrados.columns:
        dias_com_dados = dados_filtrados[coluna] != 0
        contagem_dias_diferentes_de_zero = dias_com_dados.groupby(
            dias_com_dados.index
        ).sum()
        dias_com_dados_por_casa[coluna] = contagem_dias_diferentes_de_zero.sum()
        consumo_medio_mensal_dict[coluna] = (
            dados_filtrados[coluna].to_numpy().sum() / dias_com_dados_por_casa[coluna]
        )

    consumo_medio_mensal = pd.DataFrame.from_dict(
        consumo_medio_mensal_dict, orient="index", columns=["Consumo(kWh)"]
    ).dropna()

    consumo_medio_mensal.reset_index(inplace=True)
    consumo_medio_mensal.rename(columns={"index": "Residência"}, inplace=True)

    residencias_sem_dados = dados_filtrados.columns[(dados_filtrados == 0).all()]
    dados_filtrados.drop(columns=residencias_sem_dados, inplace=True)

    for residencia in dados_filtrados.columns.dropna():
        nome_pessoa = residencia.replace(" (kWh)", "")
        st.subheader(f"{nome_pessoa}: R${dados_filtrados[residencia].sum():.2f}")

        consumo_total_mensal = dados_filtrados[residencia].sum()

