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
# Tech Challenge #01 - Grupo 27 - Análise de Oportunidades / Vinícolas
by. Eduardo Gomes, Igor Brito e Gabriel Pehls
""")     

with st.expander("Mais detalhes"):
    st.info("""
        Para iniciar nossas análises e entender o contexto em que está inserida a vinícola, utilizamos os dados da [Vitivinicultura](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02), disponibilizados na descrição do tech challenge. 
        Dentro da base do conjunto de dados explorados, temos o histórico anual de vendas por país em quantidade de litros (KG), que nos gráficos, mudamos para (L) e o valor em dólares (USD), que nos mostram uma visão geral das exportações da vinícola em questão.
        Com base nos gráficos disponibilizados a seguir, podemos extrair as seguintes informações para maximizar as exportações da vinícola:
        - Identificar os países de maior destaque em exportações (em Quantidade Total de Vendas);
        - Identificar países com maior valor médio por litro;
        - Avaliar a evolução das exportações ao longo dos anos;
        A partir destes dados, podemos começar a explorar novas bases de dados (demográficos,  climáticos, econômicos e de avaliações de vinhos) para entender como esses fatores externos podem nos trazer indicadores dos potenciais países que temos que maximizar, manter ou reduzir esforços em relação às exportações.    
    """,
        icon="ℹ️"
    )

# Layout do aplicativo
tab_geral, tab_paises_exportacoes, tab_top10_exportacoes, tab_reviews, tab_reviews_opportunity, tab_consideracoes_finais = st.tabs(["Geral","Exportações por País", "Top 10 Exportações","Avaliações de Vinhos","Avaliações de Vinhos - oportunidades", "Considerações Finais"])

with tab_geral:
    st.plotly_chart(
    generate_graphs._exportacao_dolar_quantidade_ano(get_data.DF_EXPORTACAO(years_to_filter))
    , use_container_width=True)

    st.write("""
                - Notamos um comportamento de crescimento, desde 2015 nos dois indicadores. 
                - No ano de 2009 existe uma quantidade em L vendidos muito maior do que nos demais anos do período estudado, além do valor em dólares exportações no ano de 2013. A Rússia foi o maior responsável por esses aumentos.
            """)

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._proporcao_valor_por_litro_vendido_pais_ano(get_data.DF_EXPORTACAO(years_to_filter))
    , use_container_width=True)

    st.write("""
                - Analisando o gráfico de valor em dólares por litro vendido por país e ano, é possível identificar os países que estão dispostos a pagar um preço mais elevado por litro de vinho. Esses países podem representar oportunidades de mercado para vinhos de alta qualidade e de maior valor agregado.
                - Países que apareceram com mais constância em países que exportaram por um valor médio mais alto em comparação aos demais nos últimos 15 anos.
                - Suiça, Canadá, Rep. Tcheca, Dinamarca*, Austrália, China.
            """)

with tab_paises_exportacoes:
    st.plotly_chart(
    generate_graphs._exportacao_vinhos_por_pais(get_data.DF_EXPORTACAO(years_to_filter))
    , use_container_width=True)

    st.write("""
                - A partir dos gráficos, é possível verificar países que o Paraguai aparece constantemente como país que mais exportou anualmente (em dólares), principalmente nos últimos 5 anos, aparecendo como país que mais exportou. Estados Unidos e Rússia também aparecem constantemente nos países que mais gastam anualmente.
                - Dentro dos anos analisados, a Rússia foi a que mais se destacou em valores gastos de maneira sazonal, em 2008 ~ (US\$ 2Mi), 2009 ~ (US\$ 6Mi), 2013 ~ (US\$ 15Mi), nos demais anos, os valores gastos foram muito mais controlados (menores que US\$ 500k).
            """)

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._quantidade_vendida_por_pais_ano(get_data.DF_EXPORTACAO(years_to_filter))
    , use_container_width=True)

    st.write("""
                - Dentro destes gráficos, notamos que o Paraguai é o país que mais exporta vinho do Brasil em quantidade de L e de forma mais constante, históricamente. 
                - A Rússia, por conta de suas compras sazonais aparece em segundo no período estudado.
            """)

with tab_top10_exportacoes:
    st.plotly_chart(
    generate_graphs._exportacoes_top10_dol(get_data.DF_EXPORTACAO(years_to_filter))
    , use_container_width=True)

    st.divider() # ------------------------------------------------------

with tab_reviews:
    st.plotly_chart(
    generate_graphs._comercio_no_rs(
        get_data.DF_WINE_SELLED(years_to_filter).head(10)
        )
    , use_container_width=True)

    st.divider() # ------------------------------------------------------
    col1, col2, col3 = st.columns([1,1,1])

    graphs_ratings = generate_graphs._wine_ratings(
        get_data.DF_WINE_RATINGS()
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

    graphs_ratings = generate_graphs._wine_ratings_opportunity(get_data.DF_WINE_RATINGS())
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
    
with tab_consideracoes_finais:
     st.write("""
     Com base nos detalhes trazidos nos gráficos anteriores, destacamos os países abaixo de acordo com perfís das vendas nos últimos 15 anos e com base nas avaliações de vinhos:

    Potenciais países para maximizar as exportações, visto que nos últimos 15 anos eles possuem valores gastos por litro acima dos demais:
    - Suíça, Canadá, República Tcheca, Dinamarca, Austrália e China

    Países que muito provavelmente possuirão menores valores de logísticas para as exportações:
    - Argentina, Uruguai, Peru e México

    Países que podem nos trazer melhores resultados nos espumantes (O produto representa 3% das vendas nos últimos 15 anos):
    - Croácia, África do Sul, Austrália (novamente), Espanha e Portugal e Israel

    Países que podem nos trazer melhores resultados em vinhos tintos (O produto representa 63% das vendas nos últimos 15 anos).
    - Ucrânia e o Egito, Peru (novamente)

    A seguir analisaremos mais profundamente estes e demais países com base em dados (climatológicos, econômicos e demográficos) para entender quais continuam sendo válidos para investirmos esforços
     """)
