import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    layout="wide",
    page_title="Início",
    page_icon=":material/bolt:",
)

st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 3rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)


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

    st.title("Consumo elétrico - Ilha das Onças")
    st.sidebar.success("Selecione uma opção acima.")

    st.markdown(
        """
        O presente dashboard contém dados acerca do consumo elétrico em uma 
        das comunidades atendidas eletricamente pelo Grupo de Estudos e Desenvolvimento de 
        Alternativas Energéticas(GEDAE) a partir de dados coletados por um medidor de consumo 
        de energia desenvolvido pelo discente do curso de bacharelado em Engenharia Elétrica da 
        UFPA [Pedro Bentes Lobato](http://lattes.cnpq.br/9753927402598189).
        \n
        O projeto "Nanorrede de Distribuição C.C. de Estrutura Aberta Aplicada a Edificações 
        Ribeirinhas da Amazônia" é coordenado pelo [Prof. Dr. Wilson Negrão Macêdo](http://lattes.cnpq.br/3386249951714088) e
        tem como objetivo demonstrar a viabilidade e sustentabilidade a longo prazo do atendimento de pequenos consumidores 
        de energia elétrica na região amazônica por meio de nanorredes de distribuição fotovoltaicas 
        em corrente contínua de estrutura aberta por meio da implementação de uma nanorrede 
        alimentada por geração fotovoltaica e pequenos bancos de baterias, a qual conta também com 
        uma embarcação elétrica de pequeno porte conhecida regionalmente como rabeta.\
        \n

        ### Quer conhecer mais sobre o grupo? 
        - Visite o nosso [site](https://www.gedae.ufpa.br/)
        - Nos siga no [Instagram](https://www.instagram.com/gedae.ufpa/)


        ### Conheça a equipe
    """
    )

    equipe = {
        "Wilson Negrão Macêdo": [
            "fotos/Wilson_Macedo.JPG",
            "Possui graduação (1999) e mestrado (2002) em Engenharia Elétrica pela Universidade Federal do Pará e Doutorado em Energia pela Universidade de São Paulo (2006), onde desenvolveu atividades de pesquisa no período de 2002 a 2006, no Laboratório de Sistemas Fotovoltaicos do Instituto de Eletrotécnica e Energia. Atualmente desenvolve trabalhos de pesquisa e inovação, na área de energia solar fotovoltaica e sistemas híbridos, no Grupo de Estudos e Desenvolvimento de Alternativas Energéticas da Universidade Federal do Pará (GEDAE/UFPA), onde coordena o Laboratório de Sistemas Fotovoltaicos. Pesquisador colaborador do Grupo de Pesquisa em Inovação, Desenvolvimento e Adaptação de Tecnologias Sustentáveis - GPIDATS - IDSM-OS.",
        ],
        "Marcos André Barros Galhardo": [
            "fotos/Marcos_Galhardo.JPG",
            "Engenheiro eletricista com doutorado em Engenharia Elétrica pela UFPA, onde é atualmente Professor Associado e pesquisador do GEDAE/UFPA. Atua principalmente nos seguintes temas: energias renováveis, qualidade da energia elétrica; micro e minigeração (conectada à rede ou isolada); minirredes de distribuição de eletricidade; sistemas híbridos para produção de eletricidade; eficiência energética em edificações; sistemas de monitoração de grandezas elétricas e ambientais; telemetria; instrumentação eletrônica.",
        ],
        "Pedro Bentes Lobato": [
            "fotos/Pedro_Lobato.JPG",
            "Aluno do Curso de Bacharelado em Engenharia Elétrica da Universidade Federal do Pará. Atualmente é bolsista de iniciação científica CNPq no Grupo de Estudos e Desenvolvimento de Alternativas Energéticas (GEDAE/UFPA), onde realiza atividades de pesquisa nas áreas de microrredes isoladas de distribuição de energia elétrica, sensoriamento de sistemas elétricos de potência, geração distribuída, mobilidade elétrica de pequeno porte e o uso de energias renováveis como forma de desenvolvimento sustentável na Amazônia.",
        ],
        "Arilson Moraes Borges": [
            "fotos/Arilson_Moraes.JPG",
            "Discente de engenharia elétrica na Universidade Federal do Pará (UFPA) e bolsista no Grupo de Estudos E Desenvolvimento de Alternativas Energéticas (GEDAE).",
        ],
        "Victor Parente de Oliveira Alves": [
            "fotos/Victor_Parente.JPG",
            "Concluiu, pela Universidade Federal do Pará (UFPA), a Graduação e Mestrado em Engenharia Elétrica. Atualmente, é doutorando pelo Programa de Pós-Graduação em Engenharia Elétrica (PPGEE) na mesma instituição. É integrante do GEDAE (Grupo de Estudos e Desenvolvimento de Alternativas Energéticas) da Universidade Federal do Pará desde 2017, onde tem a oportunidade de atuar em projetos de diferentes naturezas. Seu interesse em pesquisa engloba as seguintes áreas: fontes renováveis de energia, sistemas isolados, sistemas em corrente contínua, eletrônica de potência e smart grids.",
        ],
        "Ilan Sampaio Lima": [
            "fotos/Ilan_Lima.JPG",
            "Discente de Engenharia Elétrica pela Universidade Federal do Pará. Atualmente, atua como bolsista de iniciação científica no GEDAE/UFPA. Possui experiência em linguagens de programação como Python e C++, uso de energias renováveis e sistemas de energia solar fotovoltaica. É membro do Grupo de Estudos e Desenvolvimento de Alternativas Energéticas (GEDAE), onde reealiza atividades de pesquisa. Como hobbies, pratica de ciclismo, dedica-se ao aprendizado de guitarra e estuda empreendedorismo, com ênfase no desenvolvimento e gestão de startups.",
        ],
    }

    for membro in equipe:
        # Cria duas colunas para a foto e a descrição
        col1, col2 = st.columns([1, 6])  # Ajuste as proporções conforme necessário

        # Coluna 1: Imagem
        with col1:
            st.image(equipe[membro][0], use_column_width=True)

        # Coluna 2: Nome e Descrição
        with col2:
            st.write(f"**{membro}**")
            st.write(equipe[membro][1])
