import pandas as pd
import matplotlib.pyplot as plt


# %% Corona Net (416 China, 102 mainland Prov)
cnet = pd.read_csv('Gov_data/coronanet_release_allvars.csv')
cnet = cnet[cnet.country == 'China']
cnet['date_start'] = cnet['date_start'].apply(pd.to_datetime)

# cnet = cnet[(cnet.date_start > '2020-01-30') & (cnet.da)]

cnet = cnet[cnet.init_country_level == 'Provincial']



a = cnet[(~cnet['event_description'].str.contains('highest level')) &
     (~cnet['event_description'].str.contains('medical team'))]




# %% ACAPS (156 China)

aps = pd.read_excel('Gov_data/ACAPS-govt-measure/acaps_covid19_government_measures_dataset.xlsx',
                    sheet_name='Database')

aps = aps[aps.COUNTRY == 'China']



# %% WHO (646 China, 194 mainland Prov)
who = pd.read_excel('Gov_data/WHO/WHO_PHSM_Cleaned_V1_20_07_01.xlsx')

who = who[who.country_territory_area == 'China']

who.loc[who.area_covered == 'Shanghai', 'admin_level'] = 'state'
who.loc[who.area_covered == 'Shanghai municipality', 'admin_level'] = 'state'
who.loc[who.area_covered == 'Beijing', 'admin_level'] = 'state'

who = who[who.admin_level == 'state']
who['date_start'] = who.date_start.apply(pd.to_datetime)

a = who.groupby('date_start').count()

who = who[(~who.area_covered.str.contains('Hong Kong')) & (~who.area_covered.str.contains('Taiwan')) & (~who.area_covered.str.contains('Macao'))]

who.groupby('area_covered').count()


# %% HIT covid (528 China, 528 mainland prov)
hit = pd.read_csv('Gov_data/hit-covid-master/data/hit-covid-longdata.csv')
hit = hit[hit.country_name == 'China']
hit.drop(['record_id', 'update', 'country', 'admin1', 'usa_county', 'usa_county_code'], axis=1)

hit.groupby('admin1_name').count()

a = hit[hit.intervention_group == 'mask']




# %% Complexity Science Hub Vienna (no China)

csh = pd.read_csv('Gov_data/covid19-interventionmeasures-master/Version1/COVID19_non-pharmaceutical-interventions.csv',
                   encoding="ISO-8859-1")

# csh = csh[csh.Country == 'China']



