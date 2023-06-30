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

paises = get_data.LISTA_PAISES(years_to_filter)
st.write("""
# Situação Macroeconômica
""")     

# add an exapnder for the user to display more info about the app
with st.expander("Mais detalhes"):
    st.info("""
    Texto bonitão aqui
    """)

# Layout do aplicativo
tab_credito_logistica, tab_logistica_pop, tab_top10_exportacoes = st.tabs(["Crédito e Abertura de Empresa","Logística e População", "Top 10 Exportações"])

with tab_credito_logistica:
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

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._exportacoes_top10_qtd(get_data.DF_EXPORTACAO(years_to_filter, paises))
    , use_container_width=True)
