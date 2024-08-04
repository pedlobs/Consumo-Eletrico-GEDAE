import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.graph_objects as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import yaml
from yaml.loader import SafeLoader


st.set_page_config(
    page_title="Curvas de carga - GEDAE",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="🔍",
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

cor_plot = {
    "Potencia(W)": "#70AD47",
    "Consumo(kWh)": "#5B9BD5",
    "Corrente RMS(A)": "#F5C767",
    "Tensao RMS(V)": "#1984A3",
}


@st.cache_data
def load_data(nomes_abas):
    sheet_name = "Dados"
    spreadsheet = client.open(sheet_name)

    # Cria o dicionário
    dfs = {}

    for aba in nomes_abas:
        sheet = spreadsheet.worksheet(aba)
        data = sheet.get_all_records()
        try:
            dfs[aba] = pd.DataFrame(data)
            dfs[aba]["Hora"] = pd.to_datetime(dfs[aba]["Hora"])
            dfs[aba].set_index(dfs[aba]["Hora"], inplace=True)
        except Exception as e:
            st.error(f"Erro ao acessar dados da aba {aba}: {e}")

    return dfs


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

    dfs = load_data(nomes_abas)

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

    # Selectbox para escolher o DataFrame a ser analisado
    residencias_escolhidas = st.sidebar.multiselect(
        "Selecione as residências", nomes_abas
    )

    if len(residencias_escolhidas) >= 2:
        parametro_selecionado = st.radio(
            "Escolha qual parâmetro comparar:",
            ["Potencia(W)", "Consumo(kWh)", "Corrente RMS(A)", "Tensao RMS(V)"],
            horizontal=True,
        )

        datas_base = dfs[residencias_escolhidas[0]].index

        for residencia in residencias_escolhidas[1:]:
            df = dfs[residencia]
            datas_base = datas_base.intersection(df.index)

        anos_em_comum = sorted(datas_base.year.unique())
        ano_selecionado = st.sidebar.selectbox("Selecione o ano", anos_em_comum)

        meses_em_comum = sorted(
            datas_base[datas_base.year == ano_selecionado].month.unique()
        )
        mes_selecionado = st.sidebar.selectbox(
            "Selecione o mês", meses_em_comum, format_func=lambda x: meses[x - 1]
        )

        dias_em_comum = sorted(
            (
                datas_base[
                    (datas_base.year == ano_selecionado)
                    & (datas_base.month == mes_selecionado)
                ].day.unique()
            )
        )
        dia_selecionado = st.sidebar.selectbox("Selecione o dia", dias_em_comum)

        for residencia in residencias_escolhidas:
            df = dfs[residencia]
            df_filtrado = df[
                (df.index.year == ano_selecionado)
                & (df.index.month == mes_selecionado)
                & (df.index.day == dia_selecionado)
            ]

            consumo = df_filtrado["Consumo(kWh)"].iloc[-1]

            plot = go.Figure()

            plot.add_trace(
                go.Scatter(
                    x=df_filtrado["Hora"],
                    y=df_filtrado[parametro_selecionado],
                    name=parametro_selecionado,
                    marker={"color": cor_plot[parametro_selecionado]},
                )
            )

            plot.update_xaxes(title_text="Hora")
            plot.update_yaxes(title_text=parametro_selecionado)
            plot.update_layout(title_text=f"{residencia} - {consumo} kWh")

            st.plotly_chart(plot)

    elif len(residencias_escolhidas) <= 1:
        st.warning("Selecione ao menos duas residências para comparar os parâmetros.")
