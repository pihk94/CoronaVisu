import numpy as np
import pandas as pd
import urllib.request
import datetime
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
def get_french_data():
    """
        Fonction permettant d'obtenir les dernières données disponibles ici :
            https://www.data.gouv.fr/en/datasets/donnees-relatives-a-lepidemie-du-covid-19/
    """
    SERIES_TEMP_DEP_NB_SERVICES = 'https://www.data.gouv.fr/en/datasets/r/c2003994-46d5-4c1b-9aa8-9ebb72fa5a2c'
    SERIES_TEMP_DEP_NB = 'https://www.data.gouv.fr/en/datasets/r/b94ba7af-c0d6-4055-a883-61160e412115'
    SERIES_TEMP_DEP_SOS_MEDECIN = 'https://www.data.gouv.fr/en/datasets/r/941ff2b4-ea24-4cdf-b0a7-655f2a332fb2'
    urllib.request.urlretrieve(SERIES_TEMP_DEP_NB_SERVICES,'Data/FR_TS_DEP_SERVICES.csv')
    urllib.request.urlretrieve(SERIES_TEMP_DEP_NB,'Data/FR_TS_DEP.csv')
    urllib.request.urlretrieve(SERIES_TEMP_DEP_SOS_MEDECIN,'Data/FR_TS_DEP_SOS_MEDECIN.xlsx')
def import_french(name,sep=';'):
    """
        Fonction permettant d'importer l'un des trois datasets  : SERIES_TEMP_DEP_NB_SERVICES , SERIES_TEMP_DEP_NB, SERIES_TEMP_DEP_SOS_MEDECIN
    """
    dic ={
        'SERIES_TEMP_DEP_NB_SERVICES' : 'Data/FR_TS_DEP_SERVICES.csv',
        'SERIES_TEMP_DEP_NB':'Data/FR_TS_DEP.csv',
        'SERIES_TEMP_DEP_SOS_MEDECIN':'Data/FR_TS_DEP_SOS_MEDECIN.xlsx'
    }
    return pd.read_csv(dic[name],sep=sep)
def get_info_data(x):
    """
        Fonction donnant les informations sur les datasets                
    """
    dic = {'SERIES_TEMP_DEP_NB_SERVICES': """
                Description:
                    Séries temporelles du nombre cumulés de services hospitaliers ayant au moins déclarés un cas de COVID-19 
                Col: 
                    dep : Département
                    jour : Jour au format DD/MM/AAAA
                    nb : Nombre cumulé de services hospitaliers ayant déclaré au moins un cas
                """,
            'SERIES_TEMP_DEP_NB': """
                Description : 
                    Séries temporelles du covid 19 en France selon les départements
                Col : 
                    dep : Département
                    sexe : Sexe de la personne (0,1,2)
                    jour : Jour au format DD/MM/AAAA
                    hosp : Nombre de personnes hospitalisées
                    rea : Nombre de personnes actuellement en réanimation ou soins intensifs
                    rad : Nombre cumulé de personnes retournées à domicile
                    dc : Nombre cumulé de personnes décédées
                """,
            'SERIES_TEMP_DEP_SOS_MEDECIN':"""
                Description : 
                    Séries temporelles du covid 19 en France selon les département
                Col :
                    dep : Departement
                    date_de_passage : Date de passage
                    sursaud_cl_age_corona : Tranche d'âge des patients
                    nbre_pass_corona : Nombre de passages aux urgences pour suspicion de COVID-19
                    nbre_pass_tot : Nombre de passages aux urgences total
                    nbre_hospit_corona : Nombre d'hospitalisations parmi les passages aux urgences pour suspicion de COVID-19
                    nbre_pass_corona_h : Nombre de passages aux urgences pour suspicion de COVID-19 - Hommes
                    nbre_pass_corona_f : Nombre de passages aux urgences pour suspicion de COVID-19 - Femmes
                    nbre_pass_tot_h : Nombre de passages aux urgences total - Hommes
                    nbre_pass_tot_f : Nombre de passages aux urgences total - Femmes
                    nbre_hospit_corona_h : Nombre d'hospitalisations parmi les passages aux urgences pour suspicion de COVID-19 - Hommes
                    nbre_hospit_corona_f : Nombre d'hospitalisations parmi les passages aux urgences pour suspicion de COVID-19 - Femmes
                    nbre_acte_corona : Nombres d'actes médicaux SOS Médecins pour suspicion de COVID-19
                    nbre_acte_tot : Nombres d'actes médicaux SOS Médecins total
                    nbre_acte_corona_h : Nombres d'actes médicaux SOS Médecins pour suspicion de COVID-19 - Hommes
                    nbre_acte_corona_f : Nombres d'actes médicaux SOS Médecins pour suspicion de COVID-19 - Femmes
                    nbre_acte_tot_h : Nombres d'actes médicaux SOS Médecins total - Hommes
                    nbre_acte_tot_f : Nombres d'actes médicaux SOS Médecins total - Femmes
            """,
            'CATEG':"""
            0	tous âges
            A	moins de 15 ans
            B	15-44 ans
            C	45-64 ans
            D	65-74 ans
            E	75 et plus 
            """

    }
    return dic[x]

df_cases_world = get_frame('Confirmed')
get_french_data()