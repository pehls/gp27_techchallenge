import streamlit as st
import pandas as pd
import config 
import generate_graphs

st.set_page_config(
    page_title="Tech Challenge #01 - Grupo 27",
    layout="wide"
)

st.sidebar.image(config.LOGO, caption='Wine Study', use_column_width=True)

st.sidebar.title("Seleção de parâmetros")

# add a slider to select time frame to get predictions
with st.sidebar.expander("Selecionar time frame"):
    global predictions_time_frame 
    predictions_time_frame = st.slider(
        "Para qual intervalo de anos quero analisar?",
        value=[1970,2023],
        step=1, min_value=1970, max_value=2023)
    
st.write("""
# Tech Challenge - vinhos
""")     

# add an exapnder for the user to display more info about the app
with st.expander("Mais detalhes"):
    st.info("""
    Texto bonitão aqui
    """)

base_path = '..\\data\\processed'

df_noaa_global = pd.read_csv(r'..\\data\\processed\\noaa_global\\noaa_global_final.csv', sep=';', decimal=',')
df_vinhos = pd.read_csv(r'..\\data\\processed\\tech_challenge\\df_vinhos.csv', sep=';', decimal=',')
df_temperature_change_data = pd.read_csv(r'..\\data\\processed\\temp_change\\temperature_change_Data.csv', sep=';', decimal=',')
df_wbpy = pd.read_csv(r'..\\data\\processed\\wbpy\\wbpy.csv', sep=';', decimal=',')

# Layout do aplicativo
tab_precipitacao, tab_temp_media, tab_temp_min, tab_temp_max = st.tabs(["Precipitação","Temperatura Média", "Temperatura Mínima", "Temperatura Máxima"])

with tab_precipitacao:
    st.plotly_chart(
    generate_graphs._metricas_noaa(df_noaa_global,'PRCP')
    , use_container_width=True)

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._density_noaa(df_noaa_global,'PRCP')
    , use_container_width=True)

with tab_temp_media:
    st.plotly_chart(
    generate_graphs._metricas_noaa(df_noaa_global,'TAVG')
    , use_container_width=True)

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._density_noaa(df_noaa_global,'TAVG')
    , use_container_width=True)

with tab_temp_min:
    st.plotly_chart(
    generate_graphs._metricas_noaa(df_noaa_global,'TMIN')
    , use_container_width=True)

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._density_noaa(df_noaa_global,'TMIN')
    , use_container_width=True)

with tab_temp_max:
    st.plotly_chart(
    generate_graphs._metricas_noaa(df_noaa_global,'TMAX')
    , use_container_width=True)

    st.divider() # ------------------------------------------------------

    st.plotly_chart(
    generate_graphs._density_noaa(df_noaa_global,'TMAX')
    , use_container_width=True)