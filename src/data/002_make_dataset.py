# -*- coding: utf-8 -*-
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import logging
import wbpy
import config
import os, glob
import time, datetime
import pandas as pd
import numpy as np
import multiprocessing as mp
import joblib

os.environ['KAGGLE_USERNAME'] = config.KAGGLE_USERNAME  #manually input My_Kaggle User_Name 
os.environ['KAGGLE_KEY'] = config.KAGGLE_KEY #

import kaggle
kaggle.api.authenticate()

def test_dir(dir):
    if not(os.path.isdir(dir)):
        os.makedirs(dir)
    return os.path.isdir(dir)

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def process_tech_challenge(logger):
    logger.info('Tech challenge data...')

    logger.info('Processing raw > interim...')
    # Ajustando dataframe das exportações
    logger.info('--Exportacoes...')

    #0. Create folder
    test_dir('data//interim//tech_challenge//')

    df_exp = pd.read_csv('data//raw//tech_challenge//ExpVinho.csv', sep=';')
    df_exp = df_exp.melt(id_vars=['Id','País'])

    vars = df_exp.variable.unique()
    valor = [x for x in vars if x.endswith('.1')]
    quantidade = list(set(vars) - set(valor))

    df_quant = df_exp.loc[df_exp['variable'].isin(quantidade)]\
        .rename(columns={
            'value':'quantidade_exportada_pais'
            , 'variable':'ano'
            , 'País':'pais'
            , 'Id':'id'
            })

    df_quant['ano'] = df_quant['ano'].astype(int)

    df_value = df_exp.loc[df_exp['variable'].isin(valor)]\
        .rename(columns={
            'value':'valor_exportado_pais'
            , 'variable':'ano'
            , 'País':'pais'
            , 'Id':'id'
            })
    df_value['ano'] = [int(x.replace('.1', '')) for x in df_value['ano']]

    df_exp = pd.merge(df_quant, df_value, on=['id','pais','ano'])[['id','pais','ano','quantidade_exportada_pais','valor_exportado_pais']]\
        .drop(columns=['id'])


    df_exp.to_csv('data//interim//tech_challenge//exportacao_vinhos.csv',index=False, sep=';', decimal=',') # export data to share with the project group members

    # Ajustando df das comercializações no RS
    logger.info('--Comercializacoes...')

    #0. Create folder
    test_dir('data//interim//tech_challenge//')

    df_com = pd.read_csv('data//raw//tech_challenge//Comercio.csv', sep=';', header=None)
    lista_anos = list(df_exp['ano'].unique())
    df_com.columns = ['id','id_produto','produto'] + lista_anos

    df_com = df_com\
        .melt(id_vars=['id','id_produto','produto'])\
        .rename(columns={
                'variable':'ano'
            , 'value':'quantidade_com_rs'
        })\
        .drop(columns=['id'])

    df_com['id_produto'] = [str(x).strip().lower() for x in df_com['id_produto']]
    df_com['produto'] = [str(x).strip().lower() for x in df_com['produto']]
    df_com['ano'] = df_com['ano'].astype(int)

    df_com.to_csv('data//interim//tech_challenge//comercio_vinhos_rs.csv',index=False, sep=';', decimal=',') # export data to share with the project group members

    # Ajustando df das produções no RS
    logger.info('--Producoes...')

    #0. Create folder
    test_dir('data//interim//tech_challenge//')

    df_prod = pd.read_csv('data//raw//tech_challenge//Producao.csv', sep=';', header=None)
    lista_anos = list(df_exp['ano'].unique())
    df_prod.columns = ['id','id_produto','produto'] + lista_anos

    df_prod = df_prod\
        .melt(id_vars=['id','id_produto','produto'])\
        .rename(columns={
            'variable':'ano'
            , 'value':'quantidade_prod_rs'
        })\
        .drop(columns=['id'])

    df_prod['id_produto'] = [str(x).strip().lower() for x in df_prod['id_produto']]
    df_prod['produto'] = [str(x).strip().lower() for x in df_prod['produto']]
    df_prod['ano'] = df_prod['ano'].astype(int)

    df_prod.to_csv('data//interim//tech_challenge//producao_vinhos_rs.csv',index=False, sep=';', decimal=',') # export data to share with the project group members

    # interim to processed
    logger.info('Processing interim > processed...')

    #0. Create folder
    test_dir('data//processed//tech_challenge//')

    df_exp = pd.read_csv('data//interim//tech_challenge//exportacao_vinhos.csv', sep=';', decimal=',')
    df_prod = pd.read_csv('data//interim//tech_challenge//producao_vinhos_rs.csv', sep=';', decimal=',')
    df_com = pd.read_csv('data//interim//tech_challenge//comercio_vinhos_rs.csv', sep=';', decimal=',')

    df_prod_com = df_prod.merge(df_com, on=['id_produto','produto','ano'], how='outer')

    df_final = df_exp.merge(df_prod_com, on='ano', how='outer')

    # traduzir country code
    dict_translates = joblib.load("data\\processed\\dict_translates.pkl")
    df_final['country_code'] = [dict_translates[x].upper() for x in df_final.pais]

    df_final.to_csv('data//processed//tech_challenge//df_vinhos.csv',index=False, sep=';', decimal=',') # export data to share with the project group members

    logger.info('-- Finished tech challenge data...')

def process_temperature_change(logger):
    logger.info("Temperature Change data...")

    # Ajustar output da mudança de temperatura
    logger.info("Processing raw > processed...")

    #0. Create folder
    test_dir('data//processed//temp_change//')

    df = pd.read_csv("data//raw//temp_change//Environment_Temperature_change_E_All_Data_NOFLAG.csv", encoding='latin-1') # csv file is encoding as latin-1 type
    df_countrycode=pd.read_csv('data//raw//temp_change//FAOSTAT_data_11-24-2020.csv') #this csv file includes ISO-3 Country Code, this mentioned in Data Wrangling 

    #1. Renaming
    df.rename(columns = {'Area':'Country Name'},inplace = True)
    df.set_index('Months', inplace=True)
    df.rename({'Dec\x96Jan\x96Feb': 'Winter', 'Mar\x96Apr\x96May': 'Spring', 'Jun\x96Jul\x96Aug':'Summer','Sep\x96Oct\x96Nov':'Fall'}, axis='index',inplace = True)
    df.reset_index(inplace = True)

    #2. Filtering 
    df = df[df['Element'] == 'Temperature change']

    #2. Drop unwanted columns from df_countrycode
    df_countrycode.drop(['Country Code','M49 Code','ISO2 Code','Start Year','End Year'],axis=1,inplace=True)
    df_countrycode.rename(columns = {'Country':'Country Name','ISO3 Code':'Country Code'},inplace=True)

    #3. Merging with df to df_country
    df = pd.merge(df, df_countrycode, how='outer', on='Country Name')

    #2. Drop unwanted columns
    df.drop(['Area Code','Months Code','Element Code','Element','Unit'],axis=1,inplace=True)

    #3.Channing dataframe organization
    df = df.melt(id_vars=["Country Code", "Country Name","Months",], var_name="year", value_name="tem_change")
    df["year"] = [i.split("Y")[-1] for i in df.year]

    df = df[df['Months']=='Meteorological year']# chose just year data
    df.drop(['Months'],axis=1,inplace=True) # dropped Months column
    df.to_csv('data//processed//temp_change//temperature_change_Data.csv',index=False, sep=';', decimal=',') # export data to share with the project group members

    logger.info('-- Finished temperature change data...')
    
def process_year(file_year='2019'):
    base_path = 'data\\raw\\noaa_global'
    dest_path = 'data\\interim\\noaa_global\\years'
    test_dir(dest_path)
    if not os.path.exists(f"{dest_path}\\{file_year}.csv"):

        start = datetime.datetime.now()

        raw_df = pd.read_csv(f"{base_path}\\ghcnd_all_years\\{file_year}.csv.gz",
                        usecols=[0,1,2,3], 
                        names=['station_id','date', 'stat', 'value'], 
                        dtype= {
                              'station_id' : str
                            , 'date': str
                            , 'stat': str
                            , 'value': np.int16
                            },
                        engine='c'
                        )
        raw_df['year'] = np.int16(file_year)
        grouped = raw_df\
            .groupby(["station_id", 'year',"stat"])\
            .agg({
                'value':('min','mean','median','max')
                })\
            .reset_index()
        grouped.columns = ["station_id", 'year',"stat", 'value_min','value_mean','value_median','value_max']
        #return grouped
        grouped.to_csv(f"{dest_path}\\{file_year}.csv", index=False, sep=';', decimal='.')
        duration = (datetime.datetime.now() - start).seconds
        print(f"{file_year} took {round(duration/60, 2)} minutes.")

def read_csv(args):
        return pd.read_csv(args, sep=';', decimal='.')

def _adjust_temperature(row, var):
    """
    vamos transformar dados em farenheidt para celsius;
    caso seja menor que -90 (menor temperatura ja encontrada no planeta, na antartida) 
    ou maior que 57 (maior temp, na california (death valley, usa)), retorna np.nan
    """
    if (row['stat'] in ['TMAX','TMIN','TAVG']):
        celsius = (row[var] - 32) * 5/9
        if ((celsius > -90) & (celsius < 57)):
            return celsius
        else:
            return np.nan
    return row[var]


def process_noaa_global(logger):
    base_path = 'data\\raw\\noaa_global'
    dest_path = 'data\\interim\\noaa_global'
    test_dir(dest_path)

    logger.info('NOAA global data...')

    logger.info('Processing raw > interim...')
    
    # Ajustando dataframe dos anos
    logger.info('--Noaa ghcnd data...')
    years = [year[:4] for year in os.listdir(f"{base_path}\\ghcnd_all_years\\")]
    years.sort()
    level_of_parallelism = mp.cpu_count()
    pool = mp.Pool(level_of_parallelism)
    pool.map(process_year, years)

    # Ajustando dataframe das estações
    logger.info('--Noaa ghcnd stations...')
    df_stations = pd.read_csv(base_path+'\\ghcnd-stations.txt', sep=';', decimal='.')
    for col in ['id','name']:
        df_stations[col] = [x.strip() for x in df_stations[col]]
    df_stations.to_csv(dest_path+'\\df_stations.csv',index=False, sep=';', decimal=',')

    logger.info('Processing interim > processed...')

    base_path = 'data\\interim\\noaa_global\\'
    dest_path = 'data\\processed\\noaa_global\\'
    test_dir(dest_path)

    df_noaa = pd.concat(map(read_csv, glob.glob(base_path+'years\\*.csv')))

    df_stations = pd.read_csv(base_path+'df_stations.csv', sep=';', decimal=',').rename(columns={'id':'station_id'})

    df_noaa_global = df_noaa.merge(df_stations)

    # traduzir latitude e longitude para country code
    dict_latlong = joblib.load("data\\processed\\dict_latlong.pkl")

    df_noaa_global['lat_long'] = [f"{x.latitude},{x.longitude}" for x in df_noaa_global.itertuples()]
    df_noaa_global = df_noaa_global.loc[df_noaa_global['lat_long'].isin(list(dict_latlong.keys()))]
    df_noaa_global = df_noaa_global.loc[df_noaa_global['stat'].isin(['TMAX','TMIN','TAVG','PRCP'])]
    df_noaa_global = df_noaa_global.loc[df_noaa_global['year'] > 1970]
    df_noaa_global['country_code'] = [dict_latlong[f"{x.latitude},{x.longitude}"].upper() for x in df_noaa_global.itertuples()]

    # filtrar apenas country que esteja no df_vinhos
    df_vinhos = pd.read_csv(r'data\\processed\\tech_challenge\\df_vinhos.csv', sep=';', decimal=',')
    df_noaa_global = df_noaa_global.loc[df_noaa_global['country_code'].isin(list(df_vinhos.country_code.unique()))]
    
    # ajuste da temperatura
    for col in ['value_min', 'value_mean', 'value_median','value_max']:
        df_noaa_global[col] = df_noaa_global.apply(lambda row: _adjust_temperature(row, col), axis=1)
        # imputar media no lugar do nan
        df_noaa_global[col] = df_noaa_global[col].fillna(df_noaa_global.groupby(['year','stat','country_code'])[col].transform('mean'))

    df_noaa.to_csv(dest_path+'noaa_global.csv', index=False, sep=';', decimal=',')

    df_noaa_global = df_noaa_global\
        .groupby(['year','stat','country_code'])\
        .agg({
            'value_min':'min'
            , 'value_mean':'mean'
            , 'value_median':'median'
            , 'value_max':'max'
        })\
        .reset_index()
    df_noaa_global\
        .to_csv(dest_path+'noaa_global_final.csv', index=False, sep=';', decimal=',')
    logger.info('-- Finished NOAA global data...')

def process_wbpy(logger):
    logger.info('WBpy data...')

    import os, glob
    import pandas as pd

    base_path = 'data\\raw\\wbpy\\'
    dest_path = 'data\\processed\\wbpy\\'
    test_dir(dest_path)

    logger.info('Processing raw > processed...')
    def read_csv(args):
        df = pd.read_csv(args, sep=',', decimal='.')
        df['metric'] = args.split('\\')[-1].split('.')[0]
        return df

    df_wbpy = pd.concat(map(read_csv, glob.glob(base_path+'*.csv'))).rename(columns={'Unnamed: 0':'year'})
    df_wbpy = df_wbpy.melt(id_vars=['year','metric']).rename(columns={'variable':'country'})
    df_wbpy.to_csv(dest_path+'wbpy.csv', index=False, sep=';', decimal=',')

    logger.info('-- Finished wbpy data...')

def finalize_process(logger):
    logger.info('Finalizing process, deleting raw data...')
    import os
    for root, dirs, files in os.walk('data\\raw', topdown=False):
        for name in files:
            if not ('ghcnd-stations.txt' in name):
                os.remove(os.path.join(root, name))
        for name in dirs:
            try:
                os.rmdir(os.path.join(root, name))
            except:
                pass

def main():
    """ Runs data processing scripts to process raw data into interim (../interim)  and from interim > processed
    """
    logger = logging.getLogger(__name__)

    process_tech_challenge(logger)

    # process_temperature_change(logger)

    process_noaa_global(logger)

    process_wbpy(logger)

    finalize_process(logger)



if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
