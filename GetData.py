import numpy as np
import pandas as pd

#def get_frame_world(name):
#    url = ('https://covid.ourworldindata.org/data/ecdc/total_'
#           f'{name}.csv')
#    df = pd.read_csv(url)
#    return df
#
#df_cases_world = get_frame_world('cases')
#df_deaths_wogfrld = get_frame_world('deaths')


URL_MAPPING_COUNTRIES = 'https://raw.githubusercontent.com/pratapvardhan/notebooks/master/covid19/mapping_countries.csv'
COL_REGION = 'Country/Region'

def get_mappings(url):
    df = pd.read_csv(url)
    return {
        'df': df,
        'replace.country': dict(df.dropna(subset=['Name']).set_index('Country')['Name']),
        'map.continent': dict(df.set_index('Name')['Continent'])
    }

def get_frame(name):
    url = (
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/'
        f'csse_covid_19_time_series/time_series_19-covid-{name}.csv')
    df = pd.read_csv(url)
    mapping = get_mappings(URL_MAPPING_COUNTRIES)
    df['Country/Region'] = df['Country/Region'].replace(mapping['replace.country'])
    return df

df_cases_world = get_frame('Confirmed')
