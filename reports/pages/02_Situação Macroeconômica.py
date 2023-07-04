import streamlit as st
import config 
import src.generate_graphs as generate_graphs
import src.get_data as get_data
from datetime import date

st.set_page_config(
    page_title="Tech Challenge #01 - Grupo 27",
    layout="wide"
)

st.sidebar.image(config.LOGO, caption='Wine Study', use_column_width=True)

st.sidebar.title("Seleção de parâmetros")

# add a slider to select time frame to get data
with st.sidebar.expander("Selecionar time frame"):
    years_to_filter = st.slider(
        "Para qual espaço de tempo quero analisar?",
        value=[15],
        step=1, min_value=1, max_value=(date.today().year - 1970))[0]

paises = list(set(get_data.LISTA_PAISES(years_to_filter)
          + ['Suíça', 'Canadá',' República Tcheca', 'Dinamarca', 'Austrália', 'China', 
             'Argentina', 'Uruguai', 'Peru', 'México',
             'Croácia', 'África do Sul', 'Austrália', 'Espanha', 'Portugal', 'Israel',
             'Ucrânia','Egito','Peru'
             ] # Países que apareceram na análise das exportações
          + ['Ucrânia','Egito','Uruguai','Portugal','Espanha','México','Israel'] # Países que apareceram na análise das avaliações
          ))
st.write("""
# Situação Macroeconômica
""")     

# add an exapnder for the user to display more info about the app
with st.expander("Mais detalhes"):
    st.info(f"""
    Seguindo em nossa análise, vamos avaliar os {len(paises)} Países encontrados na análise climática, avaliações dos vinhos, ou nos dados de exportação, quanto a alguns indicadores macroeconômicos:
    - Para tal, utilizaremos Indicadores disponíveis no [WBPY](https://pypi.org/project/wbpy/), uma biblioteca disponível em Python, que nos trás os dados da api do [World Bank](https://documents.worldbank.org/en/publication/documents-reports/api), uma instituição mundial, com 189 países membros, e escritórios em 130 locais diferentes.
    - Podemos consultar todos os indicadores disponíveis [aqui](http://api.worldbank.org/v2/indicator), mas nos concentraremos em alguns:
        - Número de procedimentos para registrar uma empresa;
        - Índice de Performance Logística;
        - Crédito Doméstico para o Setor Privado;
        - Crescimento populacional
    - Também utilizaremos o total em dólares e de Litros exportados, vindos do [site da vitivinicultura da Embrapa](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01)
    """,
        icon="ℹ️"
    )

# Layout do aplicativo
tab_credito, tab_logistica_pop, tab_top10_exportacoes, tab_consideracoes_finais = st.tabs(["Crédito e Abertura de Empresa","Logística e População", "Top 10 Exportações", "Considerações Finais"])

with tab_credito:
        
    st.plotly_chart(
        generate_graphs._credito_top10(get_data.DF_WBPY(years_to_filter, paises))
        , use_container_width=True
    )

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
        generate_graphs._register_business_top10(get_data.DF_WBPY(years_to_filter, paises))
        , use_container_width=True
    )

with tab_logistica_pop:
        
    st.plotly_chart(
        generate_graphs._crescimento_pop_top10(get_data.DF_WBPY(years_to_filter, paises))
        , use_container_width=True
    )

    st.divider() # ------------------------------------------------------
    col1, col2 = st.columns([1,3])
    with col1:
        st.plotly_chart(
            generate_graphs._logistic_groups(get_data.DF_WBPY(years_to_filter, paises))
            , use_container_width=True
        )
    
    with col2:
        st.plotly_chart(
            generate_graphs._logistic_bests(get_data.DF_WBPY(years_to_filter, paises))
            , use_container_width=True
        )

with tab_top10_exportacoes:
        
    st.plotly_chart(
    generate_graphs._exportacoes_top10_dol(get_data.DF_EXPORTACAO(years_to_filter, paises))
    , use_container_width=True)

    st.write(f"""
             - Destacamos aqui a pequena presença nos países da África do Sul, India, Áustria, Equador, Nova Caledônia, Malta, México, Nova Zelândia, Peru, Colômbia, Argentina e Venezuela;
             - Os países da América do sul, em específico, poderiam ser ótimos alvos, pela facilidade em logística e proximidade;
             - Ilhas Marshall, Peru, Bolívia, Equador, Colômbia, África do Sul, Argentina e Nova Zelândia ainda despontam com um crescimento populacional excelente;
             - Ao analisarmos a Performance Logística, temos a presença da Áustria, Suíça, Dinamarca, Finlândia, Reino Unido e Suécia, como integrantes da melhor faixa do índice;
             - Reino Unido, Austrália, Dinamarca, Suíça, Nova Zelândia, Hong Kong, Ilhas Marshall e Portugal ainda pontuam por estarem dentro do top 10 de países com maior crédito para o setor privado;
             - Nova Zelândia, de forma disparada, possui a menor burocracia para abertura de empresas, estando a Austrália, México, Nova Caledônia, Hong Kong, Suécia e Dinamarca dentro do top 10 novamente.
             """)
    st.divider() # ------------------------------------------------------

with tab_consideracoes_finais:
    st.write(f"""
             - Dos países analisados inicialmente, notamos que a China, Espanha e Reino Unido já possuem uma grande quantidade (e também valor) total de exportações acima de 1MM;
             - O foco em ampliar o mercado, portanto, deveria ser na outra ponta do gráfico na seção "Top 10 Exportações", em países como Argentina, Peru, Uruguai e México, mas também Croácia, África do Sul, Índia, Áustria, Malta, Nova Zelândia e Nova Caledônia;
             - A Oportunidade em alavancar os ganhos pode estar em países como Suíça, Canadá, Polônia, Finlândia, Argentina e Itália, que aparentemente pagam melhor (ou seja, o Total em Dólares despenca como maior do que os vizinhos pela quantidade, o retorno seria maior);
             - Para nossos Espumantes, o crescimento seria excepcional em países como Croácia, África do Sul e Austrália - sendo que África do Sul e Austrália possuem pouca burocracia para a abertura de empresas, estando a Austrália em um posicionamento interessante de concessão de crédito ao setor privado;
             - Ainda nos Espumantes, as avaliações médias de Israel, Austrália, Espanha, Portugal e África do Sul estão bem próximas do Brasil;
             - O Peru se destaca pelo crescimento de sua população, bem como facilidade em logística, além de ter pontuações médias nos tipos branco e tinto menores que o Brasil!
             """)