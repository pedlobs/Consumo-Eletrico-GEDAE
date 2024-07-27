import streamlit as st
import pandas as pd
import plotly.express as px
# import plotly.graph_objects as go
import os


st.set_page_config(
    page_title="Consumo Elétrico - GEDAE",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="📊",
    # page_icon="logoGEDAE.png",
)


@st.cache_data
def load_data(pasta):
    lista = []
    for arquivo in os.listdir(pasta):
        nome = arquivo.replace(".csv", "")
        dir_arquivo = os.path.join(pasta, arquivo)
        try:  # Evita erros de codificação ao ler os arquivos CSV
            df = pd.read_csv(
                dir_arquivo,
                sep=";",
                encoding="utf-8",
                parse_dates=["Data"],
                dayfirst=True,
            )
        except UnicodeDecodeError:
            df = pd.read_csv(
                dir_arquivo,
                sep=";",
                encoding="ISO-8859-1",
                parse_dates=["Data"],
                dayfirst=True,
            )
        df.set_index("Data", inplace=True)
        df.rename(columns={"Consumo(kWh)": f"{nome} (kWh)"}, inplace=True)
        lista.append(df)
        df = pd.concat(lista, axis=1).fillna(0)
    return df


# Carregaa dados da pasta "Dados"
pasta_dados = "Dados"
dados = load_data(pasta_dados)

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
    f"Consumo Elétrico Ilha das Onças - {meses[mes_selecionado-1]} {ano_selecionado}"
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

# Criando o gráfico de pizza
fig_pizza = px.pie(
    consumo_medio_mensal,
    values="Consumo(kWh)",
    names="Residência",
    title="Distribuição Percentual do Consumo Médio Diário",
    color="Residência",
)

st.plotly_chart(fig_pizza)

residencias_sem_dados = dados_filtrados.columns[(dados_filtrados == 0).all()]
dados_filtrados.drop(columns=residencias_sem_dados, inplace=True)

for residencia in dados_filtrados.columns.dropna():
    st.subheader(residencia.replace(" (kWh)", ""))

    consumo_total_mensal = dados_filtrados[residencia].sum()

    fig_barras = px.bar(
        dados_filtrados[residencia],
        # x='Data',
        y=residencia,
        # color='Consumo(kWh)',
        # color_continuous_scale='Viridis',
        title=f"Energia mensal consumida: {consumo_total_mensal:.2f} kWh",
    )

    fig_barras.update_layout(
        xaxis_title="Data", yaxis_title="Consumo (kWh)", template="plotly_white"
    )

    st.plotly_chart(fig_barras)