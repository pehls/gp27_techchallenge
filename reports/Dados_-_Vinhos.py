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
    Texto bonitão aqui
    """)

# Layout do aplicativo
tab_geral, tab_paises_exportacoes, tab_top10_exportacoes, tab_reviews, tab_consideracoes_finais = st.tabs(["Geral","Exportações por País", "Top 10 Exportações","Avaliações de Vinhos", "Considerações Finais"])

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
    generate_graphs._comercio_no_rs(get_data.DF_WINE_SELLED(years_to_filter).head(10))
    , use_container_width=True)

    st.divider() # ------------------------------------------------------
    col1, col2, col3, col4 = st.columns([1,1,1,1])

    graphs_ratings = generate_graphs._wine_ratings(get_data.DF_WINE_RATINGS(years_to_filter))
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
    
    with col4:
        st.plotly_chart(
        graphs_ratings[3]
        , use_container_width=True)