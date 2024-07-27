import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="Curvas de carga - GEDAE",
    # layout="wide",
    initial_sidebar_state="auto",
    page_icon="📈",
    # page_icon="logoGEDAE.png",
)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
)

nome, status_login, user = authenticator.login()


if status_login == False:
    st.error("Usuário/Senha incorreto")
if status_login == None:
    st.warning("Digite seu login e senha")
if status_login:
    authenticator.logout('Logout', 'sidebar')
    
    st.write("# Página em desenvolvimento...:male-mechanic:")