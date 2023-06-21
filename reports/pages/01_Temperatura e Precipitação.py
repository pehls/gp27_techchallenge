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

base_path = '..\\data\\processed'

# Layout do aplicativo
tab_precipitacao, tab_temp_media, tab_temp_min, tab_temp_max = st.tabs(["Precipitação","Temperatura Média", "Temperatura Mínima", "Temperatura Máxima"])

with tab_precipitacao:
    st.plotly_chart(
    generate_graphs._metricas_noaa(get_data.DF_NOAA_GLOBAL(years_to_filter),'PRCP')
    , use_container_width=True)

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._density_noaa(get_data.DF_NOAA_GLOBAL(years_to_filter),'PRCP')
    , use_container_width=True)

with tab_temp_media:
    st.plotly_chart(
    generate_graphs._metricas_noaa(get_data.DF_NOAA_GLOBAL(years_to_filter),'TAVG')
    , use_container_width=True)

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._density_noaa(get_data.DF_NOAA_GLOBAL(years_to_filter),'TAVG')
    , use_container_width=True)

with tab_temp_min:
    st.plotly_chart(
    generate_graphs._metricas_noaa(get_data.DF_NOAA_GLOBAL(years_to_filter),'TMIN')
    , use_container_width=True)

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._density_noaa(get_data.DF_NOAA_GLOBAL(years_to_filter),'TMIN')
    , use_container_width=True)

with tab_temp_max:
    st.plotly_chart(
    generate_graphs._metricas_noaa(get_data.DF_NOAA_GLOBAL(years_to_filter),'TMAX')
    , use_container_width=True)

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._density_noaa(get_data.DF_NOAA_GLOBAL(years_to_filter),'TMAX')
    , use_container_width=True)