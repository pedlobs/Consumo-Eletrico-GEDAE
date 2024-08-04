import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import yaml
from yaml.loader import SafeLoader
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Curvas de carga - GEDAE",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="📊🔍",
    # page_icon="logoGEDAE.png",
)

st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(sheet_name):
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    df["Data"] = pd.to_datetime(df["Data"])
    df.set_index("Data", inplace=True)
    return df


with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"], st.secrets["cookies"]["name"], st.secrets["cookies"]["key"]
)

nome, status_login, user = authenticator.login()

if status_login == False:
    st.error("Usuário/Senha incorreto")
if status_login == None:
    st.warning("Digite seu login e senha")
if status_login:
    authenticator.logout("Logout", "sidebar")

    # Credenciais da api do google
    creds_json = {
        "type": st.secrets["google_sheets"]["type"],
        "project_id": st.secrets["google_sheets"]["project_id"],
        "private_key_id": st.secrets["google_sheets"]["private_key_id"],
        "private_key": st.secrets["google_sheets"]["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["google_sheets"]["client_email"],
        "client_id": st.secrets["google_sheets"]["client_id"],
        "auth_uri": st.secrets["google_sheets"]["auth_uri"],
        "token_uri": st.secrets["google_sheets"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["google_sheets"][
            "auth_provider_x509_cert_url"
        ],
        "client_x509_cert_url": st.secrets["google_sheets"]["client_x509_cert_url"],
    }
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
    client = gspread.authorize(creds)

    # Carrega os dados da planilha do google
    nomes_abas = ["Sr João", "Sr Matoso", "Sr Yuri", "Sr Raul", "Sr Bruno"]

    sheet_name = "Dados"
    dados = load_data(sheet_name)

    colunas = dados.columns

    parametro_selecionado = st.sidebar.radio(
        "Escolha o parâmetro:",
        ["Consumo(kWh)", "Potencia(W)", "Corrente RMS(A)", "Tensao RMS(V)"],
        horizontal=False,
    )

    if parametro_selecionado in ["Potencia(W)", "Corrente RMS(A)", "Tensao RMS(V)"]:
        st.title("Em desenvolvimento...")
        for residencia in nomes_abas:
            break
            st.subheader(residencia)
            df = dfs[residencia]

            # fig = go.Figure(data=[go.Histogram(x=df[parametro_selecionado], nbinsx=20)])
            # fig.update_layout(bargap=0)
            fig = px.histogram(df, x=parametro_selecionado, nbins=30, marginal="violin")
            fig.update_yaxes(title_text="Frequência")
            st.plotly_chart(fig)

    else:
        for residencia in colunas:
            st.subheader(residencia.replace(" (kWh)", ""))
            df = dados[residencia]
            df = df.loc[(df != 0)]

            fig = px.histogram(df, marginal="box")

            st.plotly_chart(fig)
            pass
