import pandas as pd
from pathlib import Path

bundle_dir = Path(__file__).parent
BASE_PATH = Path.cwd() / bundle_dir

def DF_EXPORTACAO(years = 15):
    df = pd.read_csv(rf'{base_path}\\interim\\tech_challenge\\exportacao_vinhos.csv', 
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
    return df


def DF_NOAA_GLOBAL(years=15):
    df = pd.read_csv(rf'{base_path}\\processed\\noaa_global\\noaa_global_final.csv', sep=';', decimal=',')

    # Find the maximum year in the dataframe
    max_year = df['year'].max()

    # Calculate the minimum year to keep based on the maximum year and 15-year threshold
    min_year = max_year - years

    # Remove the records with years earlier than the minimum year
    df = df[df['year'] >= min_year]
    return df

import os
str = f"""
cwd={os.getcwd()}\n
base_path={BASE_PATH}\n
list={os.listdir(BASE_PATH / 'data/processed' )}
"""
raise Exception(str)

DF_VINHOS = pd.read_csv(rf'{base_path}\processed\tech_challenge\df_vinhos.csv', sep=';', decimal=',')

DF_TEMP_CHANGE = pd.read_csv(rf'{base_path}\processed\temp_change\temperature_change_Data.csv', sep=';', decimal=',')

def DF_WBPY(years=15):
    df = pd.read_csv(rf'{base_path}\processed\wbpy\wbpy.csv', sep=';', decimal=',')

    # Find the maximum year in the dataframe
    max_year = df['year'].max()

    # Calculate the minimum year to keep based on the maximum year and 15-year threshold
    min_year = max_year - years

    # Remove the records with years earlier than the minimum year
    df = df[df['year'] >= min_year]
    return df