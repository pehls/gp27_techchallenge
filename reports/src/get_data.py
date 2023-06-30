import pandas as pd
import numpy as np
import config 
import streamlit as st

@st.cache_data
def DF_EXPORTACAO(years = 15, paises=[]):
    df = pd.read_csv(config.BASE_PATH /'interim/tech_challenge/exportacao_vinhos.csv', 
                                sep=';', skiprows=1,
                                names=['Country', 'Year', 'Quantity (L)', 'Sales (Dollars)'])

    # Convert 'Sales (Dollars)' and 'Quantity (Kgs)' columns to numeric
    df['Sales (Dollars)'] = pd.to_numeric(df['Sales (Dollars)'], errors='coerce')
    df['Quantity (L)'] = pd.to_numeric(df['Quantity (L)'], errors='coerce')

    # Convert 'Year' column to numeric
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    # Find the maximum year in the dataframe
    max_year = df['Year'].max()

    # Calculate the minimum year to keep based on the maximum year and 15-year threshold
    min_year = max_year - years

    # Remove the records with years earlier than the minimum year
    df = df[df['Year'] >= min_year]

    # Filter only countries being analyzed
    if (len(paises)>0):
        df = df.loc[df['Country'].isin(paises)]

    return df

@st.cache_data
def DF_NOAA_GLOBAL(years=15):
    df = pd.read_csv(config.BASE_PATH /'processed/noaa_global/noaa_global_final.csv', sep=';', decimal=',')

    df = df.dropna()
    # Find the maximum year in the dataframe
    max_year = df['year'].max()

    # Calculate the minimum year to keep based on the maximum year and 15-year threshold
    min_year = max_year - years

    # Remove the records with years earlier than the minimum year
    df = df[df['year'] >= min_year]

    # Reverse country_code to country name
    df['country_code'] = [DICT_TRANSLATES_INVERTED()[country_code].replace("Marshall, Ilhas","Ilhas Marshall") for country_code in df['country_code']]
    return df

# DF_VINHOS = pd.read_csv(BASE_PATH /'processed/tech_challenge/df_vinhos.csv', sep=';', decimal=',')

# DF_TEMP_CHANGE = pd.read_csv(BASE_PATH /'processed/temp_change/temperature_change_Data.csv', sep=';', decimal=',')

@st.cache_data
def DF_WBPY(years=15, paises=[]):
    df = pd.read_csv(config.BASE_PATH /'processed/wbpy/wbpy.csv', sep=';', decimal=',')
     
    # Find the maximum year in the dataframe
    max_year = df['year'].max()

    # Calculate the minimum year to keep based on the maximum year and 15-year threshold
    min_year = max_year - years

    # Remove the records with years earlier than the minimum year
    df = df[df['year'] >= min_year]
    # Filter countries in the shared dictionary
    df = df.loc[df['country'].isin(list([x.upper() for x in DICT_TRANSLATES_INVERTED().keys()]))]

    # Reverse country_code to country name
    df['country'] = [DICT_TRANSLATES_INVERTED()[country_code].replace("Marshall, Ilhas","Ilhas Marshall") for country_code in df['country']]
    
    # Filter only countries being analyzed
    if (len(paises)>0):
        df = df.loc[df['country'].isin(paises)]
    
    return df

@st.cache_data
def DF_RS(years=15):
    df = pd.read_csv(config.BASE_PATH /'processed/inmet/rs_final.csv', sep=';', decimal=',')

    # Find the maximum year in the dataframe
    max_year = df['year'].max()

    # Calculate the minimum year to keep based on the maximum year and 15-year threshold
    min_year = max_year - years

    # Remove the records with years earlier than the minimum year
    df = df[df['year'] >= min_year]
    return df

@st.cache_data
def DF_PRECP_COMPARATIVE(df_clima_rs, df_noaa_global, stat='PRCP', thresold_filter = 3, years_to_filter=15):
    # Primeiro, recuperamos a variavel a ser analisada
    df_precp_global = df_noaa_global.loc[df_noaa_global['stat']==stat]
    # vamos remover paises com menos de {espaco de tempo/3} pontos de dados
    list_paises = (df_precp_global.dropna(axis=0).country_code.value_counts().reset_index())
    list_paises.columns=['country_code','count']
    list_paises = list(list_paises.query(f'count > {years_to_filter/2}').country_code)
    df_precp_global = df_precp_global[['year','country_code', config.DICT_Y[stat][0]]]
    df_precp_global = df_precp_global.loc[df_precp_global.year >= min(df_clima_rs.year)]
    df_precp_global = df_precp_global.loc[df_precp_global.year <= max(df_clima_rs.year)]
    df_precp_global = df_precp_global.loc[df_precp_global.country_code.isin(list_paises)]
    df_clima_rs = df_clima_rs.rename(columns={stat:config.DICT_Y[stat][0]})
    df_clima_rs['country_code'] = 'BR-RS'
    # e criamos um dataframe com todos os dados
    df_full = pd.concat([df_precp_global.loc[~df_precp_global['country_code'].isin(['BR'])]])
    # Vamos calcular o erro absoluto percentual com relação ao valor max, min e medio do RS
    def _mape(real, comparado):
        return list(abs(np.array(real) - comparado)/comparado)

    _max_precip = max(df_clima_rs[config.DICT_Y[stat][0]])
    _min_precip = min(df_clima_rs[config.DICT_Y[stat][0]])
    _mean_precip = np.mean(df_clima_rs[config.DICT_Y[stat][0]])

    # para cada bloco, 
    # 1 - calculamos o ape
    df_full['dif_perc_max'] = _mape(df_full[config.DICT_Y[stat][0]], _max_precip)
    # 2 - ranqueamos, para cada ano
    df_full['rank_per_max_year'] = df_full.groupby('year')['dif_perc_max'].rank(method="dense")
    # 3 - somamos os ranks, a menor soma vai ser o pais mais bem colocado
    final_rank_max = df_full.groupby(['country_code']).agg({'rank_per_max_year':'sum'}).reset_index()
    # 4 -e ranqueamos novamente para filtrar mais pra frente
    final_rank_max['final_rank_max'] = final_rank_max['rank_per_max_year'].rank(method="dense")
    df_full = df_full.drop(columns=['rank_per_max_year']).merge(final_rank_max.drop(columns=['rank_per_max_year']))

    df_full['dif_perc_min'] = _mape(df_full[config.DICT_Y[stat][0]], _min_precip)
    df_full['rank_per_min_year'] = df_full.groupby('year')['dif_perc_min'].rank(method="dense")
    final_rank_max = df_full.groupby(['country_code']).agg({'rank_per_min_year':'sum'}).reset_index()
    final_rank_max['final_rank_min'] = final_rank_max['rank_per_min_year'].rank(method="dense")
    df_full = df_full.drop(columns=['rank_per_min_year']).merge(final_rank_max.drop(columns=['rank_per_min_year']))

    df_full['dif_perc_mean'] = _mape(df_full[config.DICT_Y[stat][0]], _mean_precip)
    df_full['rank_per_mean_year'] = df_full.groupby('year')['dif_perc_mean'].rank(method="dense")
    final_rank_max = df_full.groupby(['country_code']).agg({'rank_per_mean_year':'sum'}).reset_index()
    final_rank_max['final_rank_mean'] = final_rank_max['rank_per_mean_year'].rank(method="dense")
    df_full = df_full.drop(columns=['rank_per_mean_year']).merge(final_rank_max.drop(columns=['rank_per_mean_year']))

    # finalmente, filtramos os 6 menores (o 1 sera sempre o proprio, esperamos)
    df_full = df_full.query(f'(final_rank_max <= {thresold_filter} or final_rank_min <= {thresold_filter}) or final_rank_mean <= {thresold_filter}')
    
    df_full = pd.concat([df_full[['year','country_code',config.DICT_Y[stat][0]]], df_clima_rs[['year','country_code',config.DICT_Y[stat][0]]]])
    df_full['stat'] = stat
    return df_full

@st.cache_data
def DICT_LATLONG():
    import joblib

    base_path = config.BASE_PATH / 'processed'
    return joblib.load(base_path / "dict_latlong.pkl")

@st.cache_data
def DICT_TRANSLATES():
    import joblib

    base_path = config.BASE_PATH / 'processed'
    return joblib.load(base_path / "dict_translates.pkl")

@st.cache_data
def DICT_TRANSLATES_INVERTED():
    import joblib

    base_path = config.BASE_PATH / 'processed'
    return {v.upper():k for k,v in joblib.load(base_path / "dict_translates.pkl").items()}

@st.cache_data
def LISTA_PAISES(years_to_filter):
    df_precp = DF_PRECP_COMPARATIVE(
                df_clima_rs=DF_RS(years_to_filter)
                , df_noaa_global=DF_NOAA_GLOBAL()
                , stat='PRCP', thresold_filter = 3
            )
    df_tavg = DF_PRECP_COMPARATIVE(
                  df_clima_rs=DF_RS(years_to_filter)
                , df_noaa_global=DF_NOAA_GLOBAL(years_to_filter)
                , stat='TAVG', thresold_filter = 6
            )
    df_tmin = DF_PRECP_COMPARATIVE(
                  df_clima_rs=DF_RS(years_to_filter)
                , df_noaa_global=DF_NOAA_GLOBAL(years_to_filter)
                , stat='TMIN', thresold_filter = 6
            )
    df_tmax = DF_PRECP_COMPARATIVE(
                  df_clima_rs=DF_RS(years_to_filter)
                , df_noaa_global=DF_NOAA_GLOBAL(years_to_filter)
                , stat='TMAX', thresold_filter = 4
            )
    
    return list(
        set(
            df_precp['country_code'].to_list() + 
            df_tavg['country_code'].to_list() +
            df_tmin['country_code'].to_list() +
            df_tmax['country_code'].to_list() 
        ) - set([
            'BR-RS'
        ]
        ))