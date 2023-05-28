# -*- coding: utf-8 -*-
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import logging
import wbpy
import config
import os
import time
import pandas as pd

os.environ['KAGGLE_USERNAME'] = config.KAGGLE_USERNAME  #manually input My_Kaggle User_Name 
os.environ['KAGGLE_KEY'] = config.KAGGLE_KEY #

import kaggle
kaggle.api.authenticate()

def test_dir(dir):
    if not(os.path.isdir(dir)):
        os.mkdir(dir)
    return os.path.isdir(dir)

def download(url = 'http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv', layer='raw'):
    import requests, os

    time.sleep(5)

    file_name = url.split('/')[-1:][0]

    test_dir(f'data\\{layer}')
    file_path = f'data\\{layer}\\{file_name}'
    if not(os.path.isfile(file_path)):
        try:
            r = requests.get(url, allow_redirects=True)
            with open(file_path, 'wb') as file:
                file.write(r.content)
        except:
            time.sleep(5)
            try:
                r = requests.get(url, allow_redirects=True)
                with open(file_path, 'wb') as file:
                    file.write(r.content)
            except:
                raise
    return file_path, os.path.isfile(file_path)

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def main():
    """ Runs data processing scripts to get raw data into (../raw)
    """
    logger = logging.getLogger(__name__)
    logger.info('Recovering raw data...')

    logger.info('Tech challenge data...')
    downloaded_files = {download(url = _url, layer='raw\\tech_challenge') for _url in config.URLS_TO_DOWNLOAD}
    for item in downloaded_files:
        if not(item[1]):
            logger.error('-- Some data failed, tryin again...')
            downloaded_files = {download(url = _url, layer='raw\\tech_challenge') for _url in config.URLS_TO_DOWNLOAD}
        else:
            logger.info('-- Tech challenge data ok...')

    logger.info('World Bank data...')
    test_dir('data\\raw\\wbpy')
    api = wbpy.IndicatorAPI()
    dict_countries = api.get_countries()
    list_of_countries = list(dict_countries.keys())
    for key in config.DICT_INDICATORS:
        list_results = []
        for countries in chunker(list_of_countries, 10):
            time.sleep(5)
            try:
                df = api.get_dataset(config.DICT_INDICATORS[key], countries, date="1970:2021")
                list_results.append(pd.DataFrame(df.as_dict()))
            except:
                print(f"error in {countries}")
            pd.concat(list_results).to_csv(f"data\\raw\\wbpy\\{key}.csv")
    logger.info('-- World Bank data ok...')

    logger.info('Kaggle data...')
    test_dir('data\\raw\\temp_change')
    # https://www.kaggle.com/datasets/sevgisarac/temperature-change
    kaggle.api.dataset_download_files('sevgisarac/temperature-change', path='data\\raw\\temp_change', unzip=True)
    # https://www.kaggle.com/datasets/noaa/noaa-global-historical-climatology-network-daily
    kaggle.api.dataset_download_files('noaa/noaa-global-historical-climatology-network-daily', path='data\\raw\\noaa_global', unzip=True)
    logger.info('-- Kaggle data ok...')
    logger.info('Finished raw data!')





if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
