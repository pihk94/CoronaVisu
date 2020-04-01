import pandas as pd
import urllib.request
from datetime import datetime

############# W O R L D   D A T A #############

URL_MAPPING_COUNTRIES = 'https://raw.githubusercontent.com/pratapvardhan/notebooks/master/covid19/mapping_countries.csv'

def get_frame(name): # Fonction permettant d'obtenir les dernières données mondiales sur le coronavirus, name peut être : 'confirmed', 'deaths', 'recovered'
    url = (
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/'
        f'csse_covid_19_time_series/time_series_covid19_{name}_global.csv')
    df = pd.read_csv(url)
    return df

def get_mappings(url): # Table de mapping
    df = pd.read_csv(url)
    return {
        'df': df,
        'replace.country': dict(df.dropna(subset=['Name']).set_index('Country')['Name']),
        'map.continent': dict(df.set_index('Name')['Continent'])
    }
    
def clean_df(name): # Fonction permettant de récupérer un dataframe clean, name peut être : 'confirmed', 'deaths', 'recovered'
    mapping = get_mappings(URL_MAPPING_COUNTRIES)
    df = get_frame(name)
    df['Country/Region'] = df['Country/Region'].replace(mapping['replace.country'])
    df['Continent'] = df['Country/Region'].map(mapping['map.continent'])
    df['Province/State'].fillna('', inplace = True)
    df = df[df['Continent'].notnull()]
    cols = ['Continent', 'Country/Region', 'Province/State', 'Lat', 'Long'] + [col for col in df if (col != 'Continent') & (col != 'Country/Region') & (col != 'Province/State') & (col !='Lat') & (col != 'Long')]
    return df[cols]

def get_subregion(name, country): # Fonction permettant de récupérer les données des sous régions d'un pays, name peut être : 'confirmed', 'deaths', 'recovered'
    df = clean_df(name)
    return df.loc[df['Country/Region'] == country]
    
def get_subcountry(name, continent): # Fonction permettant de récupérer les données des sous pays d'un continent, name peut être : 'confirmed', 'deaths', 'recovered'
    df = clean_df(name)
    return df.loc[df['Continent'] == continent]

def get_recap_by_country(date, previous = 1): # Fonction permettant de récupérer un tableau récapitulatif par pays à une date donnée, previous = nb de jours de comparaison par rapport à la date donnée
    
    dft_confirmed = clean_df('confirmed')
    dft_death = clean_df('deaths')
    dft_recovered = clean_df('recovered')
    
    if date == 'today':
        date = pd.to_datetime(datetime.now())
        date_t = date - pd.to_timedelta(1, unit = 'd')
        date_t_1 = date_t - pd.to_timedelta(previous, unit = 'd')
        date_t = '/'.join(str(x) for x in (date_t.month, date_t.day, 20))
        date_t_1 = '/'.join(str(x) for x in (date_t_1.month, date_t_1.day, 20))
    else:
        date_t = pd.to_datetime(date)
        date_t_1 = date_t - pd.to_timedelta(previous, unit = 'd')
        date_t = '/'.join(str(x) for x in (date_t.month, date_t.day, 20))
        date_t_1 = '/'.join(str(x) for x in (date_t_1.month, date_t_1.day, 20))
        
    dfc_confirmed_t = dft_confirmed.groupby('Country/Region')[date_t].sum()
    dfc_death_t = dft_death.groupby('Country/Region')[date_t].sum()
    dfc_recovered_t = dft_recovered.groupby('Country/Region')[date_t].sum()
    
    dfc_confirmed_t_1 = dft_confirmed.groupby('Country/Region')[date_t_1].sum()
    dfc_death_t_1 = dft_death.groupby('Country/Region')[date_t_1].sum()
    dfc_recovered_t_1 = dft_recovered.groupby('Country/Region')[date_t_1].sum()
    
    df_table = (pd.DataFrame(dict(Cases=dfc_confirmed_t, ActiveCases = dfc_confirmed_t - dfc_recovered_t, Deaths=dfc_death_t, Recovered=dfc_recovered_t, PCases=dfc_confirmed_t_1, PDeaths=dfc_death_t_1, PRecovered=dfc_recovered_t_1))
             .sort_values(by=['Cases', 'Deaths', 'Recovered'], ascending=[False, False, False])
             .reset_index())
    df_table.rename(columns={'index': 'Country/Region'}, inplace=True)
    for c in 'Cases, Deaths, Recovered'.split(', '):
        df_table[f'{c} (+)'] = (df_table[c] - df_table[f'P{c}']).clip(0)
    df_table.drop(['PCases', 'PDeaths', 'PRecovered'], axis = 1, inplace = True)
    df_table['Fatality Rate'] = (100 * df_table['Deaths'] / df_table['Cases']).round(1)
    
    return df_table
    
def get_recap_by_continent(date, previous = 1): # Fonction permettant de récupérer un tableau récapitulatif par continent à une date donnée, previous = nb de jours de comparaison par rapport à la date donnée
    
    dft_confirmed = clean_df('confirmed')
    dft_death = clean_df('deaths')
    dft_recovered = clean_df('recovered')
    
    if date == 'today':
        date = pd.to_datetime(datetime.now())
        date_t = date - pd.to_timedelta(1, unit = 'd')
        date_t_1 = date_t - pd.to_timedelta(previous, unit = 'd')
        date_t = '/'.join(str(x) for x in (date_t.month, date_t.day, 20))
        date_t_1 = '/'.join(str(x) for x in (date_t_1.month, date_t_1.day, 20))
    else:
        date_t = pd.to_datetime(date)
        date_t_1 = date_t - pd.to_timedelta(previous, unit = 'd')
        date_t = '/'.join(str(x) for x in (date_t.month, date_t.day, 20))
        date_t_1 = '/'.join(str(x) for x in (date_t_1.month, date_t_1.day, 20))
        
    dfc_confirmed_t = dft_confirmed.groupby('Continent')[date_t].sum()
    dfc_death_t = dft_death.groupby('Continent')[date_t].sum()
    dfc_recovered_t = dft_recovered.groupby('Continent')[date_t].sum()
    
    dfc_confirmed_t_1 = dft_confirmed.groupby('Continent')[date_t_1].sum()
    dfc_death_t_1 = dft_death.groupby('Continent')[date_t_1].sum()
    dfc_recovered_t_1 = dft_recovered.groupby('Continent')[date_t_1].sum()
    
    df_table = (pd.DataFrame(dict(Cases=dfc_confirmed_t, ActiveCases = dfc_confirmed_t - dfc_recovered_t, Deaths=dfc_death_t, Recovered=dfc_recovered_t, PCases=dfc_confirmed_t_1, PDeaths=dfc_death_t_1, PRecovered=dfc_recovered_t_1))
             .sort_values(by=['Cases', 'Deaths', 'Recovered'], ascending=[False, False, False])
             .reset_index())
    df_table.rename(columns={'index': 'Continent'}, inplace=True)
    for c in 'Cases, Deaths, Recovered'.split(', '):
        df_table[f'{c} (+)'] = (df_table[c] - df_table[f'P{c}']).clip(0)
    df_table.drop(['PCases', 'PDeaths', 'PRecovered'], axis = 1, inplace = True)
    df_table['Fatality Rate'] = (100 * df_table['Deaths'] / df_table['Cases']).round(1)
    
    return df_table

############# F R E N C H   D A T A #############
    
SERIES_TEMP_DEP_NB_SERVICES = 'https://www.data.gouv.fr/en/datasets/r/c2003994-46d5-4c1b-9aa8-9ebb72fa5a2c'
SERIES_TEMP_DEP_NB = 'https://www.data.gouv.fr/en/datasets/r/b94ba7af-c0d6-4055-a883-61160e412115'
SERIES_TEMP_DEP_SOS_MEDECIN = 'https://www.data.gouv.fr/en/datasets/r/941ff2b4-ea24-4cdf-b0a7-655f2a332fb2'

def get_french_data(): # Fonction permettant d'obtenir les dernières données disponibles ici : https://www.data.gouv.fr/en/datasets/donnees-relatives-a-lepidemie-du-covid-19/
    urllib.request.urlretrieve(SERIES_TEMP_DEP_NB_SERVICES,'Data/FR_TS_DEP_SERVICES.csv')
    urllib.request.urlretrieve(SERIES_TEMP_DEP_NB,'Data/FR_TS_DEP.csv')
    urllib.request.urlretrieve(SERIES_TEMP_DEP_SOS_MEDECIN,'Data/FR_TS_DEP_SOS_MEDECIN.xlsx')
    
def import_french(name,sep=';'): # Fonction permettant d'importer l'un des trois datasets : SERIES_TEMP_DEP_NB_SERVICES, SERIES_TEMP_DEP_NB, SERIES_TEMP_DEP_SOS_MEDECIN
    dic = {
        'SERIES_TEMP_DEP_NB_SERVICES' : 'Data/FR_TS_DEP_SERVICES.csv',
        'SERIES_TEMP_DEP_NB':'Data/FR_TS_DEP.csv',
        'SERIES_TEMP_DEP_SOS_MEDECIN':'Data/FR_TS_DEP_SOS_MEDECIN.xlsx'}
    return pd.read_csv(dic[name],sep=sep)

def get_info_data(x): # Fonction donnant les informations sur les datasets                
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
