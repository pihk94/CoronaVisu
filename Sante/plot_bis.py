from GetData import * 
import plotly.graph_objects as go
from plotly.offline import plot
import numpy as np
import pandas as pd

URL_MAPPING_COUNTRIES = 'https://raw.githubusercontent.com/pratapvardhan/notebooks/master/covid19/mapping_countries.csv'

mapping = get_mappings(URL_MAPPING_COUNTRIES)
df_cases_world = get_frame('confirmed')
df_cases_world.rename(columns = {'Country/Region' : 'Country'}, inplace = True)
df_cases_world = df_cases_world.merge(mapping['df'], on = 'Country')
df_cases_world['region'] = df_cases_world['Country/Region'] + '-' + df_cases_world['Province/State'].fillna('')
df_cases_world.drop(['Province/State', '])

lst = []
for pays in df_cases_world.region.unique():
    for col in df_cases_world.columns[4:-2]:
        nb = df_cases_world.set_index('region')[col][pays]
        continent = df_cases_world.set_index('region')['continent'][pays]
        lat = df_cases_world.set_index('region')['Lat'][pays]
        lon = df_cases_world.set_index('region')['Long'][pays]
        lst += [(pays,col,nb,continent,lat,lon)]
df_ = pd.DataFrame(lst, columns=['region', 'date', 'nombre', 'continent', 'lat', 'lon'])
df_.replace(-1, 0, inplace = True)

df_['text'] = df_['region'] + '<br>Confirmés: ' + (df_['nombre']).astype(str)
limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
countries = []

continent_list = df_['continent'].unique()
df_['date'] = pd.to_datetime(df_['date'])
df_ = df_[(df_['date'].dt.year == 2020) & (df_['date'].dt.month == 3)]
df_['date'] = df_['date'].dt.day
j=0
data=[]

for i in continent_list:
    df_sub = df_[df_['continent']==i]
    data += [go.Scattergeo(
        lon = df_sub['lon'],
        lat = df_sub['lat'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['nombre'],
            sizeref=2.*max(df_sub['nombre'])/(25.**2),
            sizemin = 3,
            color = colors[j],
            line_color = 'rgb(40,40,40)',
            line_width = 0.5,
            sizemode = 'area'),
        name = i)]
    layout = go.Layout()   
    sliders = [dict(steps= [dict(method= 'animate',
                           args= [[df_sub['date'] ],
                                  dict(mode= 'immediate',
                                  frame= dict( duration=100, redraw= True ),
                                           transition=dict(duration= 300)
                                          )
                                    ],
                            label='{:d}'.format(k)
                             ) for k in df_sub['date']], 
                transition= dict(duration= 0 ),
                x=0,#slider starting position  
                y=0, 
                currentvalue=dict(font=dict(size=12), 
                                  prefix='Date: ', 
                                  visible=True, 
                                  xanchor= 'center'),  
                len=1.0
                )
           ]
    layout.update(updatemenus=[dict(type='buttons', showactive=True,
                                y=0,
                                x=1.05,
                                xanchor='right',
                                yanchor='top',
                                pad=dict(t=0, r=10),
                                buttons=[dict(label='Play',
                                              method='animate',
                                              args=[None, 
                                                    dict(frame=dict(duration=100, 
                                                                    redraw=True),
                                                         transition=dict(duration=0),
                                                         fromcurrent=False,
                                                         mode='immediate'
                                                        )
                                                   ]
                                             )
                                        ]
                               )
                          ],
              sliders=sliders);
    j+=1
fig=go.Figure(data=data, layout=layout)
plot(fig)
