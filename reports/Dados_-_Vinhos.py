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
    
st.write("""
# Tech Challenge - vinhos
""")     

# add an exapnder for the user to display more info about the app
with st.expander("Mais detalhes"):
    st.info("""
    Perante a necessidade de encontrarmos possíveis países em que possamos abrir novos negócios, aumentando a presença da empresa de forma internacional, através da exportação de vinhos, iremos analisar diversos aspectos, como:
    - Exportações atuais, através da quantidade de litros e do valor monetário atribuído;
    - Histórico de exportações, nos últimos 15 anos;
    - Avaliações gerais de vinhos no mundo (destacando algumas oportunidades);
    - Temperatura e precipitação histórica, em busca de climas parecidos com o do estado do RS, para uma melhor visualização de oportunidades de ampliação da exportação dos produtos produzidos com maior volume atualmente;
    - Análise da situação dos países que foram destacados, encontrando locais com maior abertura de crédito a empresas privadas, com menos burocracia para abertura de empresas, maior qualidade de cadeia logística e um crescimento populacional interessante, bem como uma busca por países com valor de venda mais positivo, e possibilidade de expansão na quantidade exportada.
    """)

# Layout do aplicativo
tab_geral, tab_paises_exportacoes, tab_top10_exportacoes, tab_reviews, tab_reviews_opportunity, tab_consideracoes_finais = st.tabs(["Geral","Exportações por País", "Top 10 Exportações","Avaliações de Vinhos","Avaliações de Vinhos - oportunidades", "Considerações Finais"])

with tab_geral:
    st.plotly_chart(
    generate_graphs._exportacao_dolar_quantidade_ano(get_data.DF_EXPORTACAO(years_to_filter))
    , use_container_width=True)

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._proporcao_valor_por_litro_vendido_pais_ano(get_data.DF_EXPORTACAO(years_to_filter))
    , use_container_width=True)

with tab_paises_exportacoes:
    st.plotly_chart(
    generate_graphs._exportacao_vinhos_por_pais(get_data.DF_EXPORTACAO(years_to_filter))
    , use_container_width=True)

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._quantidade_vendida_por_pais_ano(get_data.DF_EXPORTACAO(years_to_filter))
    , use_container_width=True)

with tab_top10_exportacoes:
    st.plotly_chart(
    generate_graphs._exportacoes_top10_dol(get_data.DF_EXPORTACAO(years_to_filter))
    , use_container_width=True)

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._exportacoes_top10_qtd(get_data.DF_EXPORTACAO(years_to_filter))
    , use_container_width=True)

with tab_reviews:
    st.plotly_chart(
    generate_graphs._comercio_no_rs(
        get_data.DF_WINE_SELLED(years_to_filter).head(10)
        )
    , use_container_width=True)

    st.divider() # ------------------------------------------------------
    col1, col2, col3 = st.columns([1,1,1])

    graphs_ratings = generate_graphs._wine_ratings(
        get_data.DF_WINE_RATINGS(years_to_filter)
        )
    with col1:
        st.plotly_chart(
        graphs_ratings[0]
        , use_container_width=True)

    with col2:
        st.plotly_chart(
        graphs_ratings[1]
        , use_container_width=True)
    
    with col3:
        st.plotly_chart(
        graphs_ratings[2]
        , use_container_width=True)
    

with tab_reviews_opportunity:
    col1, col2, col3 = st.columns([1,1,1])

    graphs_ratings = generate_graphs._wine_ratings_opportunity(get_data.DF_WINE_RATINGS(years_to_filter))
    with col1:
        st.plotly_chart(
        graphs_ratings[0]
        , use_container_width=True)

        st.write(f"""
                 - Ao Analisarmos o vinho branco, notamos a presença da Argentina, Uruguai e Peru, como evidência, tendo em vista sua presença na América do Sul, e consequentemente, o menor valor em logística para exportação. 
                 - O México também aparece, com Avaliações muito próximas às do Brasil, representando um local interessante para exportarmos Vinho Branco, tendo uma competitividade interessante.
                 - Ainda, temos a Croácia, com avaliações de vinhos um pouco melhores que o Brasil, e provavelmente um custo maior de exportação; 
                 """)

    with col2:
        st.plotly_chart(
        graphs_ratings[1]
        , use_container_width=True)

        st.write(f"""
                 - Nos Espumantes, notamos países como África do Sul e Austrália, que tem características climáticas semelhantes ao Rio Grande do Sul, com notas bem próximas ao Brasil;
                 - A Espanha e Portugal possuem uma proximidade Cultural e Geográfica interessantes;
                 - Israel apresenta avaliações bem melhores que o nosso país, mas dentro da faixa de 15%;
                 """)
    
    with col3:
        st.plotly_chart(
        graphs_ratings[2]
        , use_container_width=True)

        st.write(f"""
                 - Nos Vinhos Tintos, destacamos a presença do Peru, um país da América do sul, com algumas pequenas semelhanças ao clima do RS, e que também possui avaliações de vinhos brancos com valor inferior ao Brasileiro;
                 - Ucrânia e Egito aparecem como surpresas, com avaliações inferiores ao Brasil; vamos analisá-las com mais profundidade na Situação Macroeconômica;
                 """)
    

