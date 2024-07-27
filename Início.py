import streamlit as st

st.set_page_config(
    # layout="wide",
    page_title="Início",
    page_icon=":material/bolt:",
)

st.write("# Consumo elétrico - Ilha das Onças")

st.sidebar.success("Selecione uma opção acima.")

st.markdown(
    """
    O presente dashboard contém dados acerca do consumo elétrico em uma 
    das comunidades atendidas eletricamente pelo Grupo de Estudos e Desenvolvimento de 
    Alternativas Energéticas(GEDAE) a partir de dados coletados por um medidor de consumo 
    de energia desenvolvido pelo discente do curso de bacharelado en Engenharia Elétrica da UFPA [Pedro Bentes Lobato](http://lattes.cnpq.br/9753927402598189).
    \n
    O projeto "Nanorrede de Distribuição C.C. de Estrutura Aberta Aplicada a Edificações 
    Ribeirinhas da Amazônia" é coordenado pelo [Prof. Dr. Wilson Negrão Macêdo](http://lattes.cnpq.br/3386249951714088)
    tem como objetivo demonstrar a viabilidade e sustentabilidade a longo prazo do atendimento de pequenos consumidores 
    de energia elétrica na região amazônica por meio de nanorredes de distribuição fotovoltaicas 
    em corrente contínua de estrutura aberta por meio da implementação de uuma nanorrede 
    alimentada por geração fotovoltaica e pequenos bancos de baterias, a qual conta também com 
    uma embarcação elétrica de pequeno porte conhecida regionalmente como rabeta.\
    \n


    **👈 Selecione uma opção para visualizar os dados**

    ### Quer conhecer mais sobre o grupo? 
    - Visite o nosso [site](https://www.gedae.ufpa.br/)
    - Nos siga no [Instagram](https://www.instagram.com/gedae.ufpa/)


    ### Conheça a equipe
    - Colocar um link para a página da equipe no futuro ou o nome da galera aqui
"""
)