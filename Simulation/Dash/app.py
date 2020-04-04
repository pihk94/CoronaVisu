import dash
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import json
import glob
import os
import pandas as pd
import numpy as np

#APP SETTINGS
external_stylesheets = [dbc.themes.BOOTSTRAP,"https://use.fontawesome.com/releases/v5.8.1/css/all.css",'https://kit.fontawesome.com/3ee914798e.js']
image_directory = 'img/icon-corona/png/'
lst_img = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# FUNCTION FOR SIMULATION
def SEIR_mano_augmented(val_init,coeff,jour_inter,t):
    """
        Input : 
            val_init : Liste de 4 valeurs initials que va prendre le modèle 
            coeff : Liste de valeurs pour Alpha,Gamma, Beta et Rho
            t :
        Output:
            
    """
    S0,E0,I0= val_init
    S,E,I,Mild,Severe,Severe_hosp,Fatal,R_mild,R_Severe,R_Fatal = [S0],[E0],[I0],[0],[0],[0],[0],[0],[0],[0]
    a,b,g,r,death_rate,D_death,p_severe,recov_mild,duree_hosp,recover_severe=coeff
    p_mild = 1 - death_rate - p_severe
    for _ in t[1:]:
        if _ < jour_inter:
            nS = S[-1] - (b*S[-1]*I[-1])
            nE = E[-1] + (b*S[-1]*I[-1]-a*E[-1])
            nI = I[-1] + (a*E[-1]-g*I[-1])
            nMild = Mild[-1] + (p_mild * g * I[-1] - (1/recov_mild) * Mild[-1]) 
            nSevere = Severe[-1] + (p_severe * g * I[-1]  - (1/duree_hosp ) * Severe[-1])
            nSevere_hosp = Severe_hosp[-1]+ ((1/duree_hosp)*Severe[-1] - (1/recover_severe) * Severe_hosp[-1])
            nFatal = Fatal[-1] + (death_rate*g*I[-1] - (1/D_death) *Fatal[-1])
            nR_mild = R_mild[-1] + ((1/recov_mild) * Mild[-1])
            nR_Severe = R_Severe[-1] + ((1/recover_severe)*Severe_hosp[-1])
            nR_Fatal = R_Fatal[-1] + ((1/D_death) * Fatal[-1])
            S.append(nS)
            E.append(nE)
            I.append(nI)
            Mild.append(nMild)
            Severe.append(nSevere)
            Severe_hosp.append(nSevere_hosp)
            Fatal.append(nFatal)
            R_mild.append(nR_mild)
            R_Severe.append(nR_Severe)
            R_Fatal.append(nR_Fatal)
        else:
            nS = S[-1] - (r*b*S[-1]*I[-1])
            nE = E[-1] + (r*b*S[-1]*I[-1]-a*E[-1])
            nI = I[-1] + (a*E[-1]-g*I[-1])
            nMild = Mild[-1] + (p_mild * g * I[-1] - (1/recov_mild) * Mild[-1]) 
            nSevere = Severe[-1] + (p_severe * g * I[-1]  - (1/duree_hosp ) * Severe[-1])
            nSevere_hosp = Severe_hosp[-1]+ ((1/duree_hosp)*Severe[-1] - (1/recover_severe) * Severe_hosp[-1])
            nFatal = Fatal[-1] + (death_rate*g*I[-1] - (1/D_death) *Fatal[-1])
            nR_mild = R_mild[-1] + ((1/recov_mild) * Mild[-1])
            nR_Severe = R_Severe[-1] + ((1/recover_severe)*Severe_hosp[-1])
            nR_Fatal = R_Fatal[-1] + ((1/D_death) * Fatal[-1])
            S.append(nS)
            E.append(nE)
            I.append(nI)
            Mild.append(nMild)
            Severe.append(nSevere)
            Severe_hosp.append(nSevere_hosp)
            Fatal.append(nFatal)
            R_mild.append(nR_mild)
            R_Severe.append(nR_Severe)
            R_Fatal.append(nR_Fatal)
    return np.stack([S,E,I,Mild,Severe,Severe_hosp,Fatal,R_mild,R_Severe,R_Fatal]).T

def simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,jour_inter,N=69000000,t=range(1,221),):
    alpha = 1/incub_time
    gamma = 1/infec_time
    beta = R0 * gamma
    rho = 1
    recov_mild =  (14 - infec_time)
    recover_severe = (31.5 - infec_time)
    Time_to_death = death_time
    D_death = Time_to_death - infec_time
    coeff = alpha, beta,gamma,rho,death_rate,D_death,p_severe,recov_mild,duree_hosp,recover_severe
    init_vals = 1-exposed/N,exposed/N,0
    df = pd.DataFrame(SEIR_mano_augmented(init_vals,coeff,jour_inter,t),columns=['S','E','I','Mild','Severe','Severe_hosp','Fatal','R_Mild','R_Severe','R_Fatal'])
    lst=[]
    for index,row in df.iterrows():
        lst+=[(round(row.S*N),'S',index)]
        lst+=[(round(row.E*N),'E',index)]
        lst+=[(round(row.I*N),'I',index)]
        lst+=[(round(row.R_Fatal*N),'Death',index)]
        lst+=[(round(N * (row.Severe_hosp + row.Fatal)),'Hospital',index)]
        lst+=[(round(N * (row.R_Mild + row.R_Severe)),'Recovered',index)]
    return pd.DataFrame(lst,columns=['Nb','Type','Idx'])


#CSS styling
style_title_slider ={
    'margin-left':'2.5em',
    'text-align':'center',
    'font-weight':'800',
    'font-size':'13.5px',
    'margin-bottom':'0px'}
style_slider_text = {
    'text-align':'left',
    'font-size':'10px',
    'color':'#888',
    'margin-left':'4em',}
style_slider = {
    'margin-left':'40px'
}
style_slider_value = {
    'color':'#555',
    'text-align':'end',
    'font-size':'10px',
    'margin-bottom':'0px'
}

app.layout = html.Div(children=[
    html.H1(children= "Simulateur COVID-19",
    style = {
        'textAlign':'center',
        'font-weight':'400px'
    }),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='Apercu')
        ],width=10),
        dbc.Col([
            dbc.Row([
                html.Span(id='NbJours',children='365 jours')
            ],className = 'justify-content-center'),
            html.Img(src=app.get_asset_url('icon-corona/png/014-quarantine.png'),
            style={'height':'32px','width':'32px','margin-left':'7em'}),
            dbc.Row([
                html.Span(children='Susceptible',style={'font-weight':'600'})
                    ]),
                    dbc.Row([
                        dbc.Col(
                            html.Img(src=app.get_asset_url('icon-corona/png/019-virus.png'),style={'height':'32px','width':'32px','margin-top':'9px'})
                            ,width = 2),
                        dbc.Col([
                            dbc.Row([html.Img(src=app.get_asset_url('icon-corona/png/sigma.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Total_Susceptible',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})],style = {'margin-top':'9px'}),
                            dbc.Row([html.Img(src=app.get_asset_url('icon-corona/png/delta.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Day_suceptible',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})]),
                        ],width =10),  
                    ]),
            dbc.Row([
                    html.Span(children='Exposé',style={'font-weight':'600'})
                ]),
                dbc.Row([
                    dbc.Col(
                        html.Img(src=app.get_asset_url('icon-corona/png/001-virus.png'),style={'height':'32px','width':'32px','margin-top':'9px'})
                        ,width = 2),
                    dbc.Col([
                        dbc.Row([html.Img(src=app.get_asset_url('icon-corona/png/sigma.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Total_Expose',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})],style = {'margin-top':'9px'}),
                        dbc.Row([html.Img(src=app.get_asset_url('icon-corona/png/delta.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Day_expose',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})]),
                    ],width =10),  
                ]),
            dbc.Row([
                html.Span(children='Infectieux',style={'font-weight':'600'})
            ]),
            dbc.Row([
                dbc.Col(
                    html.Img(src=app.get_asset_url('icon-corona/png/044-cold.png'),style={'height':'32px','width':'32px','margin-top':'9px'})
                    ,width = 2),
                dbc.Col([
                    dbc.Row([html.Img(src=app.get_asset_url('icon-corona/png/sigma.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Total_Infect',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})],style = {'margin-top':'9px'}),
                    dbc.Row([html.Img(src=app.get_asset_url('icon-corona/png/delta.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Day_infect',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})]),
                ],width =10),  
            ]),
             dbc.Row([
                html.Span(children='Rétabli',style={'font-weight':'600'})
            ]),
            dbc.Row([
                dbc.Col(
                    html.Img(src=app.get_asset_url('icon-corona/png/049-nurse.png'),style={'height':'32px','width':'32px','margin-top':'9px'})
                    ,width = 2),
                dbc.Col([
                    dbc.Row([html.Img(src=app.get_asset_url('icon-corona/png/sigma.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Total_Recover',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})],style = {'margin-top':'9px'}),
                    dbc.Row([html.Img(src=app.get_asset_url('icon-corona/png/delta.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Day_recover',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})]),
                ],width =10)]), 
            dbc.Row([
                html.Span(children='Hospitalisation',style={'font-weight':'600'})
            ]),
            dbc.Row([
                dbc.Col(
                    html.Img(src=app.get_asset_url('icon-corona/png/healthcare-and-medical.png'),style={'height':'32px','width':'32px','margin-top':'9px'})
                    ,width = 2),
                dbc.Col([
                    dbc.Row([html.Img(src=app.get_asset_url('icon-corona/png/sigma.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Total_Hosp',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})],style = {'margin-top':'9px'}),
                    dbc.Row([html.Img(src=app.get_asset_url('icon-corona/png/delta.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Day_hosp',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})]),
                ],width =10), 
            ]),
            dbc.Row([
                html.Span(children='Décès',style={'font-weight':'600'})
            ]),
            dbc.Row([
                dbc.Col(
                    html.Img(src=app.get_asset_url('icon-corona/png/grave.png'),style={'height':'32px','width':'32px','margin-top':'9px'})
                    ,width = 2),
                dbc.Col([
                    dbc.Row([html.Img(src=app.get_asset_url('icon-corona/png/sigma.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Total_Deces',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})],style = {'margin-top':'9px'}),
                    dbc.Row([html.Img(src=app.get_asset_url('icon-corona/png/delta.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Day_deces',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})]),
                ],width =10),]),
            html.Div([
                
            ])
            
        ],width = 2)
    ]),
    dbc.Row([
        dbc.Col([
            html.H6('Variables de transmission :',
            style={'text-align':'left',
            'margin-bottom':'2em',
            'padding':'4px',
            'margin-left':'2em',
            'border-bottom': '2px solid #999'}),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        html.Label('Taux de reproduction de base R0 :',
                        style=style_title_slider),
                        html.P("Le nombre moyen d'individus qu'une personne infecte, tant qu'elle sera contagieuse.",
                        style=style_slider_text),
                        ]),
                    html.P(id='Value_R0',style=style_slider_value),
                    dcc.Slider(
                        id='R0_slider',
                        min = 0.1,
                        max = 10,
                        value=3.2,
                        step=0.1
                        ),
                    dbc.Row([
                        html.Label('Nombre de personnes infectées :'
                        ,style=style_title_slider)
                    ]),
                    dbc.Row(
                        html.P("Personnes initialement malades dans la population.",
                            style=style_slider_text)
                    ),
                    html.P(id='Value_infected',style=style_slider_value),
                    dcc.Slider(
                        id='N_malade_slider',
                        min=1,
                        max = 6000,
                        value=1,
                        step=1
                        )
                        ],width=6),
                dbc.Col([
                    dbc.Row([
                        html.Label("Durée d'incubation : ",
                        style=style_title_slider),
                        ]),
                    dbc.Row(
                            html.P("La durée moyenne d'incubation du virus.",
                                style=style_slider_text)
                    ),
                    html.P(id='Value_incub',style=style_slider_value),
                    dcc.Slider(
                        id='incub_time_slide',
                        min=0.1,
                        max = 24,
                        value=5,
                        step=0.2
                        ),
                    dbc.Row([
                        html.Label("Durée d'infectuosité : ",
                        style = style_title_slider),
                    ]),
                    dbc.Row(    
                        html.P("La durée moyenne d'infection du COVID-19.",
                        style=style_slider_text)
                    ),
                    html.P(id='Value_infect',style=style_slider_value),
                    dcc.Slider(
                        id = 'infect_time_slide',
                        min=0.1,
                        max = 24,
                        value=11,
                        step = 0.2)
                    ],
                    width=6),
            ])
        ],width = 6),
            dbc.Col([html.H6('Variables cliniques :',
                style={'text-align':'left',
                'margin-bottom':'2em',
                'padding':'4px',
                'margin-left':'2em',
                'margin-right':'4em',
                'border-bottom': '2px solid #999'}),
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            html.Label('Taux de décès :',
                            style=style_title_slider),
                        ]),
                        dbc.Row(
                            html.P("Propotion moyenne d'individus pouvant décèder du COVID-19.",
                            style=style_slider_text),
                        ),
                        html.P(id='Value_death_rate',style=style_slider_value),
                        dcc.Slider(
                            id='death_rate_slide',
                            min=0.01,
                            max = 1,
                            value=0.02,
                            step=0.01
                            ),
                        dbc.Row([
                            html.Label('Durée de fatalité :',
                            style=style_title_slider),
                        ]),
                        dbc.Row(
                            html.P("Nombre de jour de la fin d'incubation au décès.",
                            style=style_slider_text),
                        ),
                        html.P(id='Value_death_time',style=style_slider_value),
                        dcc.Slider(
                            id='Death_time_slide',
                            min=0.1,
                            max = 100,
                            value=32,
                            step=0.2
                            ),
                        ],width = 6),
                    dbc.Col([
                        dbc.Row([
                            html.Label('Taux de cas sévère :',
                            style=style_title_slider),
                        ]),
                        dbc.Row(
                            html.P("Taux d'hospitalisation sévère.",
                            style=style_slider_text),
                        ),
                        html.P(id='Value_severe',style=style_slider_value),
                        dcc.Slider(
                            id='Severe_slide',
                            min=0.1,
                            max = 1,
                            value=0.2,
                            step=0.01
                            ),
                        dbc.Row([
                            html.Label("Durée d'hospitalisation :",
                            style=style_title_slider),
                        ]),
                        dbc.Row(
                            html.P("Durée moyenne d'hospitalisation pour les cas sévères.",
                            style=style_slider_text),
                        ),
                        html.P(id='Value_duree_hosp',style=style_slider_value),
                        dcc.Slider(
                            id='Duree_hosp_slide',
                            min=1,
                            max = 100,
                            value=5,
                            step=1
                            ),
                    ],width = 6)]),
            ],width = 6)],style ={
                'margin-right':'2em'
            }),
    dbc.Row([
        dbc.Col(width=2),
        dbc.Col([
            html.H6('Distanciation sociale :',
                style={'text-align':'left',
                'margin-bottom':'2em',
                'padding':'4px',
                'margin-left':'2em',
                'margin-right':'4em',
                'border-bottom': '2px solid #999'}),
            dbc.Row([
                            html.Label('Coefficient de distanciation sociale :',
                            style=style_title_slider),
                        ]),
                        dbc.Row(
                            html.P("Taux de distanciation sociale où 100% est une distance sociale nulle et 0% une quarantaine totale.",
                            style=style_slider_text),
                        ),
                        html.P(id='Value_dist',style=style_slider_value),
                        dcc.Slider(
                            id='Dist_slide',
                            min=0.01,
                            max = 1,
                            value=0.8,
                            step=0.01
                            ),
            dbc.Row([
                            html.Label('Mise en place de la distanciation :',
                            style=style_title_slider),
                        ]),
                        dbc.Row(
                            html.P("Jour où la distanciation sociale est mise en place.",
                            style=style_slider_text),
                        ),
                        html.P(id='Value_jour_dist',style=style_slider_value),
                        dcc.Slider(
                            id='Dist_jour_slide',
                            min=1,
                            max = 220,
                            value=100,
                            step=1
                            ),
        ],width=8),
        dbc.Col(width=2),
    ])
    ])

# Figure callback
@app.callback(
    Output('Apercu','figure'),
    [Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value'),
    Input('death_rate_slide','value'),
    Input('Death_time_slide','value'),
    Input('Severe_slide','value'),
    Input('Duree_hosp_slide','value'),
    Input('Dist_slide','value'),
    Input('Dist_jour_slide','value')]
)
#R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,N=69000000,rho,t=range(1,221),jour_inter
def update_figure(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
    return  {
        'data' :[
            {'x':sim.Idx.unique(),'y':sim[sim.Type == 'Death'].Nb,'type':'bar',
            'width':'0.7',
            'name':'Décès',"hoverinfo": "none",'marker':{'color':'rgba(56, 108, 176,0.6)'}},
            {'x':sim.Idx.unique(),'y':sim[sim.Type == 'Hospital'].Nb,'type':'bar',
            'width':'0.7',
            'name':'Hospitalisation',"hoverinfo": "none",'marker':{'color':'rgba(141, 160, 203,0.6)'}},
            {'x':sim.Idx.unique(),'y':sim[sim.Type == 'I'].Nb,'type':'bar',
            'width':'0.7',
            'name':'Infectieux',"hoverinfo": "none",'marker':{'color':'rgba(237, 2, 128, 0.6)'}},
            {'x':sim.Idx.unique(),'y':sim[sim.Type == 'E'].Nb,'type':'bar',
            'width':'0.7',
            'name':'Exposé',"hoverinfo": "none",'marker':{'color':'rgba(253, 192, 134, 0.6)'}},
            
        ],
        'layout':{
            'barmode':'stack',
            'xaxis':{'type':'category',
            'dtick':'20'},
            
        }
    }
# Slider display text 
@app.callback(
    Output('Value_dist','children'),
    [Input('Dist_slide','value')]
)
def update_dist_display(value):
    return '{}%'.format(round(value*100,2))
@app.callback(
    Output('Value_jour_dist','children'),
    [Input('Dist_jour_slide','value')]
)
def update_dist_jour_display(value):
    if value >1:
        return '{} jours'.format(value)
    else:
        return '{} jour'.format(value)
@app.callback(
    Output('Value_R0','children'),
    [Input('R0_slider','value')]
)
def update_R0_display(value):
    return '{}'.format(value)
@app.callback(
    Output('Value_infect','children'),
    [Input('infect_time_slide','value')]
)
def update_infect_display(value):
    if value >1:
        return '{} jours'.format(value)
    else:
        return '{} jour'.format(value)
@app.callback(
    Output('Value_incub','children'),
    [Input('incub_time_slide','value')]
)
def update_incub_display(value):
    if value >1:
        return '{} jours'.format(value)
    else:
        return '{} jour'.format(value)
@app.callback(
    Output('Value_infected','children'),
    [Input('N_malade_slider','value')]
)
def update_infected_display(value):
    if value >1:
        return '{} infectés'.format(value)
    else:
        return '{} infecté'.format(value)
@app.callback(
    Output('Value_death_rate','children'),
    [Input('death_rate_slide','value')]
)
def update_death_rate_display(value):
    return '{} %'.format(round(value*100,2))
@app.callback(
    Output('Value_death_time','children'),
    [Input('Death_time_slide','value')]
)
def update_death_time_display(value):
    if value >1:
        return '{} jours'.format(value)
    else:
        return '{} jour'.format(value)
@app.callback(
    Output('Value_severe','children'),
    [Input('Severe_slide','value')]
)
def update_severe_display(value):
    return '{}%'.format(round(value*100,2))
@app.callback(
    Output('Value_duree_hosp','children'),
    [Input('Duree_hosp_slide','value')]
)
def update_jour_hosp_display(value):
    if value >1:
        return '{} jours'.format(value)
    else:
        return '{} jour'.format(value)
#right text display slider value and graph value

@app.callback(
    Output('NbJours','children'),
    [Input("Apercu","hoverData")]
)
def display_jour(hoverData):
    try:
        x = hoverData['points'][0]['x']
        if x == 1:
            return '1 jour'
        else:
            return str(int(x)) + ' jours'
    except:
        return '220 jours'
# TOTAL
@app.callback(
    Output('Total_Susceptible','children'),
    [Input("Apercu","hoverData"),
    Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value'),
    Input('death_rate_slide','value'),
    Input('Death_time_slide','value'),
    Input('Severe_slide','value'),
    Input('Duree_hosp_slide','value'),
    Input('Dist_slide','value'),
    Input('Dist_jour_slide','value')
    ]
)
def display_Nb_Total_susceptible(hoverData,R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    try:
        x = hoverData['points'][0]['x']
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        sim = sim[(sim.Type == 'S')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(x)].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        sim = sim[(sim.Type == 'S')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(m)].Nb))
@app.callback(
    Output('Total_Expose','children'),
    [Input("Apercu","hoverData"),
    Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value'),
    Input('death_rate_slide','value'),
    Input('Death_time_slide','value'),
    Input('Severe_slide','value'),
    Input('Duree_hosp_slide','value'),
    Input('Dist_slide','value'),
    Input('Dist_jour_slide','value')
    ]
)
def display_Nb_Total_exposed(hoverData,R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    try:
        x = hoverData['points'][0]['x']
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        sim = sim[(sim.Type == 'E')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(x)].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        sim = sim[(sim.Type == 'E')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(m)].Nb))
@app.callback(
    Output('Total_Infect','children'),
    [Input("Apercu","hoverData"),
    Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value'),
    Input('death_rate_slide','value'),
    Input('Death_time_slide','value'),
    Input('Severe_slide','value'),
    Input('Duree_hosp_slide','value'),
    Input('Dist_slide','value'),
    Input('Dist_jour_slide','value')
    ]
)
def display_Nb_Total_infect(hoverData,R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    try:
        x = hoverData['points'][0]['x']
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        sim = sim[(sim.Type == 'I')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(x)].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        sim = sim[(sim.Type == 'I')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(m)].Nb))
@app.callback(
    Output('Total_Recover','children'),
    [Input("Apercu","hoverData"),
    Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value'),
    Input('death_rate_slide','value'),
    Input('Death_time_slide','value'),
    Input('Severe_slide','value'),
    Input('Duree_hosp_slide','value'),
    Input('Dist_slide','value'),
    Input('Dist_jour_slide','value')
    ]
)
def display_Nb_Total_recov(hoverData,R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    try:
        x = hoverData['points'][0]['x']
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        sim = sim[(sim.Type == 'Recovered')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(x)].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        sim = sim[(sim.Type == 'Recovered')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(m)].Nb))
@app.callback(
    Output('Total_Hosp','children'),
    [Input("Apercu","hoverData"),
    Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value'),
    Input('death_rate_slide','value'),
    Input('Death_time_slide','value'),
    Input('Severe_slide','value'),
    Input('Duree_hosp_slide','value'),
    Input('Dist_slide','value'),
    Input('Dist_jour_slide','value')
    ]
)
def display_Nb_Total_hosp(hoverData,R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    try:
        x = hoverData['points'][0]['x']
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        sim = sim[(sim.Type == 'Hospital')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(x)].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        sim = sim[(sim.Type == 'Hospital')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(m)].Nb))
@app.callback(
    Output('Total_Deces','children'),
    [Input("Apercu","hoverData"),
    Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value'),
    Input('death_rate_slide','value'),
    Input('Death_time_slide','value'),
    Input('Severe_slide','value'),
    Input('Duree_hosp_slide','value'),
    Input('Dist_slide','value'),
    Input('Dist_jour_slide','value')
    ]
)
def display_Nb_Total_death(hoverData,R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    try:
        x = hoverData['points'][0]['x']
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        sim = sim[(sim.Type == 'Death')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(x)].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        sim = sim[(sim.Type == 'Death')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(m)].Nb))
## day
@app.callback(
    Output('Day_suceptible','children'),
    [Input("Apercu","hoverData"),
    Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value'),
    Input('death_rate_slide','value'),
    Input('Death_time_slide','value'),
    Input('Severe_slide','value'),
    Input('Duree_hosp_slide','value'),
    Input('Dist_slide','value'),
    Input('Dist_jour_slide','value')
    ]
)
def display_Nb_Day_susceptible(hoverData,R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    try:
        x = hoverData['points'][0]['x']
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        sim = sim[(sim.Type == 'S')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(x)].Nb - sim.iloc[int(x)-1].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        sim = sim[(sim.Type == 'S')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(m)].Nb - sim.iloc[int(m)-1].Nb))

@app.callback(
    Output('Day_expose','children'),
    [Input("Apercu","hoverData"),
    Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value'),
    Input('death_rate_slide','value'),
    Input('Death_time_slide','value'),
    Input('Severe_slide','value'),
    Input('Duree_hosp_slide','value'),
    Input('Dist_slide','value'),
    Input('Dist_jour_slide','value')
    ]
)
def display_Nb_Day_susceptible(hoverData,R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    try:
        x = hoverData['points'][0]['x']
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        sim = sim[(sim.Type == 'E')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(x)].Nb - sim.iloc[int(x)-1].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        sim = sim[(sim.Type == 'E')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(m)].Nb - sim.iloc[int(m)-1].Nb))

@app.callback(
    Output('Day_infect','children'),
    [Input("Apercu","hoverData"),
    Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value'),
    Input('death_rate_slide','value'),
    Input('Death_time_slide','value'),
    Input('Severe_slide','value'),
    Input('Duree_hosp_slide','value'),
    Input('Dist_slide','value'),
    Input('Dist_jour_slide','value')
    ]
)
def display_Nb_Day_infectieux(hoverData,R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    try:
        x = hoverData['points'][0]['x']
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        sim = sim[(sim.Type == 'I')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(x)].Nb - sim.iloc[int(x)-1].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        sim = sim[(sim.Type == 'I')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(m)].Nb - sim.iloc[int(m)-1].Nb))
@app.callback(
    Output('Day_recover','children'),
    [Input("Apercu","hoverData"),
    Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value'),
    Input('death_rate_slide','value'),
    Input('Death_time_slide','value'),
    Input('Severe_slide','value'),
    Input('Duree_hosp_slide','value'),
    Input('Dist_slide','value'),
    Input('Dist_jour_slide','value')
    ]
)
def display_Nb_Day_recovered(hoverData,R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    try:
        x = hoverData['points'][0]['x']
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        sim = sim[(sim.Type == 'Recovered')].set_index('Idx')
        return '{:,}'.format((sim.iloc[int(x)].Nb - sim.iloc[int(x)-1].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        sim = sim[(sim.Type == 'Recovered')].set_index('Idx')
        return '{:,}'.format((sim.iloc[int(m)].Nb - sim.iloc[int(m)-1].Nb))
@app.callback(
    Output('Day_hosp','children'),
    [Input("Apercu","hoverData"),
    Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value'),
    Input('death_rate_slide','value'),
    Input('Death_time_slide','value'),
    Input('Severe_slide','value'),
    Input('Duree_hosp_slide','value'),
    Input('Dist_slide','value'),
    Input('Dist_jour_slide','value')
    ]
)
def display_Nb_day_hosp(hoverData,R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    try:
        x = hoverData['points'][0]['x']
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        sim = sim[(sim.Type == 'Hospital')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(x)].Nb - sim.iloc[int(x)-1].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        sim = sim[(sim.Type == 'Hospital')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(m)].Nb - sim.iloc[int(m)-1].Nb))
@app.callback(
    Output('Day_deces','children'),
    [Input("Apercu","hoverData"),
    Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value'),
    Input('death_rate_slide','value'),
    Input('Death_time_slide','value'),
    Input('Severe_slide','value'),
    Input('Duree_hosp_slide','value'),
    Input('Dist_slide','value'),
    Input('Dist_jour_slide','value')
    ]
)
def display_Nb_day_death(hoverData,R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    try:
        x = hoverData['points'][0]['x']
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        sim = sim[(sim.Type == 'Death')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(x)].Nb - sim.iloc[int(x)-1].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        sim = sim[(sim.Type == 'Death')].set_index('Idx')
        return '{:,}'.format(int(sim.iloc[int(m)].Nb - sim.iloc[int(m)-1].Nb))
if __name__ == '__main__':
    app.run_server(debug=True)