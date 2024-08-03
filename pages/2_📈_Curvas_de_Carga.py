import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import yaml
from yaml.loader import SafeLoader


st.set_page_config(
    page_title="Curvas de carga - GEDAE",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="📈",
    # page_icon="logoGEDAE.png",
)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)


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

    # Sidebar para selecionar o mês e ano
    st.sidebar.title("Navegação")

    # Selectbox para escolher o DataFrame a ser analisado
    residencia_escolhida = st.sidebar.selectbox("Selecione a residência", nomes_abas)

    dados = dfs[residencia_escolhida]

    # Obter os meses e anos únicos dos dados
    meses_disponiveis = sorted(dados.index.month.unique())
    anos_disponiveis = sorted(dados.index.year.unique())

    ano_selecionado = st.sidebar.selectbox("Selecione o ano", anos_disponiveis)
    mes_selecionado = st.sidebar.selectbox(
        "Selecione o mês", meses_disponiveis, format_func=lambda x: meses[x - 1]
    )
    
    # Título do Dashboard
    st.title(f"Curvas de carga - {meses[mes_selecionado-1]} {ano_selecionado}")

    # Filtrar dados para o mês e ano selecionados
    dados_filtrados = dados[
        (dados.index.month == mes_selecionado) & (dados.index.year == ano_selecionado)
    ]

    # Obter os dias únicos com dados
    dias_disponiveis = dados_filtrados["Hora"].index.date
    dias_disponiveis = dados_filtrados["Hora"].dt.day.unique()
    dias_disponiveis.sort()

    # Seletor de dias no corpo principal da página
    dia_selecionado = st.sidebar.selectbox("Selecione o Dia", dias_disponiveis)

    dia_selecionado = dados_filtrados[dados_filtrados.index.day == dia_selecionado]

    consumo = dia_selecionado["Consumo(kWh)"].iloc[-1]
    data = dia_selecionado.iloc[0]["Hora"].strftime("%d/%m/%Y")
    nome = f"Consumo {residencia_escolhida} {data} \t Consumo={consumo:.3f} kWh"

    # Cria o subplot
    plot = make_subplots(
        rows=2,
        cols=2,
        # subplot_titles=("Potência", "Consumo", "Corrente", "Tensão"),
    )

    # Adiciona os subplots
    plot.add_trace(
        go.Scatter(
            x=dia_selecionado["Hora"],
            y=dia_selecionado["Potencia(W)"],
            name="Potencia(W)",
            marker={"color": "#70AD47"},
        ),
        row=1,
        col=1,
    )
    plot.add_trace(
        go.Scatter(
            x=dia_selecionado["Hora"],
            y=dia_selecionado["Consumo(kWh)"],
            name="Consumo(kWh)",
            marker={"color": "#5B9BD5"},
        ),
        row=1,
        col=2,
    )
    plot.add_trace(
        go.Scatter(
            x=dia_selecionado["Hora"],
            y=dia_selecionado["Corrente RMS(A)"],
            name="Corrente RMS(A)",
            marker={"color": "#F5C767"},
        ),
        row=2,
        col=1,
        # secondary_y=False
    )
    plot.add_trace(
        go.Scatter(
            x=dia_selecionado["Hora"],
            y=dia_selecionado["Tensao RMS(V)"],
            name="Tensao RMS(V)",
            marker={"color": "#1984A3"},
        ),
        row=2,
        col=2,
    )

    # Atualiza os exios x
    plot.update_xaxes(title_text="Hora", row=1, col=1)
    plot.update_xaxes(title_text="Hora", row=1, col=2)
    plot.update_xaxes(title_text="Hora", row=2, col=1)
    plot.update_xaxes(title_text="Hora", row=2, col=2)
    plot.update_xaxes(
        mirror=True,
        ticks="outside",
        showline=True,
        linecolor="Black",
        gridcolor="White",
    )

    # Atualiza os exios y
    plot.update_yaxes(title_text="Potência (W)", row=1, col=1)
    plot.update_yaxes(title_text="Consumo (kWh)", row=1, col=2)
    plot.update_yaxes(title_text="Corrente (A)", row=2, col=1)
    plot.update_yaxes(title_text="Tensão (V)", row=2, col=2)
    plot.update_yaxes(
        mirror=True,
        ticks="outside",
        showline=True,
        linecolor="black",
        gridcolor="lightgrey",
    )

    # Atualiza o layout do plot
    plot.update_layout(title_text=nome, height=700)
    plot.update_layout(plot_bgcolor="white")
    plot.update_layout(
        legend=dict(orientation="h", yanchor="middle", y=-0.25, xanchor="center", x=0.5)
    )

    # Exibe o gráfico na tela
    st.plotly_chart(plot)
