import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
from app import app
from apps import sidebar
#fct

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

def simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,jour_inter,N=69000000,t=range(1,366),):
    alpha = 1/incub_time
    gamma = 1/infec_time
    beta = R0 * gamma
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
### simulator

sim = [dbc.Row([
        dbc.Col([
            dcc.Graph(id='Apercu')
        ],width=10),
        dbc.Col([
            dbc.Row([
                html.Span(id='NbJours',children='365 jours')
            ]),
            html.Img(src=app.get_asset_url('png/014-quarantine.png'),
            style={'height':'32px','width':'32px','margin-left':'1em','margin-bottom':'1em'}),
            dbc.Row([
                html.Span(children='Susceptible',style={'font-weight':'600'})
                    ]),
                    dbc.Row([
                        dbc.Col(
                            html.Img(src=app.get_asset_url('png/019-virus.png'),style={'height':'32px','width':'32px','margin-top':'9px'})
                            ,width = 2),
                        dbc.Col([
                            dbc.Row([html.Img(src=app.get_asset_url('png/sigma.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Total_Susceptible',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})],style = {'margin-top':'9px'}),
                            dbc.Row([html.Img(src=app.get_asset_url('png/delta.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Day_suceptible',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})]),
                        ],width =10),  
                    ]),
            dbc.Row([
                    html.Span(children='Exposed',style={'font-weight':'600'})
                ]),
                dbc.Row([
                    dbc.Col(
                        html.Img(src=app.get_asset_url('png/001-virus.png'),style={'height':'32px','width':'32px','margin-top':'9px'})
                        ,width = 2),
                    dbc.Col([
                        dbc.Row([html.Img(src=app.get_asset_url('png/sigma.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Total_Expose',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})],style = {'margin-top':'9px'}),
                        dbc.Row([html.Img(src=app.get_asset_url('png/delta.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Day_expose',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})]),
                    ],width =10),  
                ]),
            dbc.Row([
                html.Span(children='Infected',style={'font-weight':'600'})
            ]),
            dbc.Row([
                dbc.Col(
                    html.Img(src=app.get_asset_url('png/044-cold.png'),style={'height':'32px','width':'32px','margin-top':'9px'})
                    ,width = 2),
                dbc.Col([
                    dbc.Row([html.Img(src=app.get_asset_url('png/sigma.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Total_Infect',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})],style = {'margin-top':'9px'}),
                    dbc.Row([html.Img(src=app.get_asset_url('png/delta.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Day_infect',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})]),
                ],width =10),  
            ]),
             dbc.Row([
                html.Span(children='Recovered',style={'font-weight':'600'})
            ]),
            dbc.Row([
                dbc.Col(
                    html.Img(src=app.get_asset_url('png/049-nurse.png'),style={'height':'32px','width':'32px','margin-top':'9px'})
                    ,width = 2),
                dbc.Col([
                    dbc.Row([html.Img(src=app.get_asset_url('png/sigma.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Total_Recover',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})],style = {'margin-top':'9px'}),
                    dbc.Row([html.Img(src=app.get_asset_url('png/delta.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Day_recover',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})]),
                ],width =10)]), 
            dbc.Row([
                html.Span(children='Hospitalised',style={'font-weight':'600'})
            ]),
            dbc.Row([
                dbc.Col(
                    html.Img(src=app.get_asset_url('png/healthcare-and-medical.png'),style={'height':'32px','width':'32px','margin-top':'9px'})
                    ,width = 2),
                dbc.Col([
                    dbc.Row([html.Img(src=app.get_asset_url('png/sigma.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Total_Hosp',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})],style = {'margin-top':'9px'}),
                    dbc.Row([html.Img(src=app.get_asset_url('png/delta.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Day_hosp',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})]),
                ],width =10), 
            ]),
            dbc.Row([
                html.Span(children='Deaths',style={'font-weight':'600'})
            ]),
            dbc.Row([
                dbc.Col(
                    html.Img(src=app.get_asset_url('png/grave.png'),style={'height':'32px','width':'32px','margin-top':'9px'})
                    ,width = 2),
                dbc.Col([
                    dbc.Row([html.Img(src=app.get_asset_url('png/sigma.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Total_Deces',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})],style = {'margin-top':'9px'}),
                    dbc.Row([html.Img(src=app.get_asset_url('png/delta.png'),style={'height':'8px','width':'8px','margin-right':'4px','margin-top':'4px','margin-left':'4px'}),html.Span(id='Day_deces',children=' xxx',style={'font-size':'12px','color':'rgb(136, 136, 136)'})]),
                ],width =10),]),
            html.Div([
                
            ])
            
        ],width = 2)
    ]),
    dbc.Row([
        dbc.Col([
            html.H6('Transmission variables :',
            style={'text-align':'left',
            'margin-bottom':'2em',
            'padding':'4px',
            'margin-left':'2em',
            'border-bottom': '2px solid #999'}),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        html.Label('Reproductible R0 :',
                        style=style_title_slider),
                        html.P("Mean number of individuals infected by one.",
                        style=style_slider_text),
                        ]),
                    html.P(id='Value_R0',style=style_slider_value),
                    dcc.Slider(
                        id='R0_slider',
                        min = 0.1,
                        max = 10,
                        value=2.5,
                        step=0.1
                        ),
                    dbc.Row([
                        html.Label('Person initialy infected:'
                        ,style=style_title_slider)
                    ]),
                    dbc.Row(
                        html.P("Person initialy infected.",
                            style=style_slider_text)
                    ),
                    html.P(id='Value_infected',style=style_slider_value),
                    dcc.Slider(
                        id='N_malade_slider',
                        min=1,
                        max = 6000,
                        value=90,
                        step=1
                        )
                        ],width=6),
                dbc.Col([
                    dbc.Row([
                        html.Label("Incubation time : ",
                        style=style_title_slider),
                        ]),
                    dbc.Row(
                            html.P("Mean incubation time.",
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
                        html.Label("Infectivity time: ",
                        style = style_title_slider),
                    ]),
                    dbc.Row(    
                        html.P("Mean infectivity time of COVID-19.",
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
        ],width = 4),
            dbc.Col([html.H6('Clinical variables :',
                style={'text-align':'left',
                'margin-bottom':'2em',
                'padding':'4px',
                'margin-left':'2em',
                'margin-right':'4em',
                'border-bottom': '2px solid #999'}),
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            html.Label('Death rate :',
                            style=style_title_slider),
                        ]),
                        dbc.Row(
                            html.P("Fatility rate of COVID-19.",
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
                            html.Label('Fatality time :',
                            style=style_title_slider),
                        ]),
                        dbc.Row(
                            html.P("Number of day from incubation to death.",
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
                            html.Label('Severe case rate:',
                            style=style_title_slider),
                        ]),
                        dbc.Row(
                            html.P("Hospitalisation rate.",
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
                            html.Label("Hospitalisation time:",
                            style=style_title_slider),
                        ]),
                        dbc.Row(
                            html.P("Hospitalisation time for severe cases.",
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
            ],width = 4),
            dbc.Col([
                html.H6('Social distancing :',
                    style={'text-align':'left',
                    'margin-bottom':'2em',
                    'padding':'4px',
                    'margin-left':'2em',
                    'margin-right':'4em',
                    'border-bottom': '2px solid #999'}),
                dbc.Row([
                                html.Label('Coefficient of social distancing :',
                                style=style_title_slider),
                            ]),
                            dbc.Row(
                                html.P("Rate where 100% is no social distancing and 0% is a total quarantine.",
                                style=style_slider_text),
                            ),
                            html.P(id='Value_dist',style=style_slider_value),
                            dcc.Slider(
                                id='Dist_slide',
                                min=0.01,
                                max = 1,
                                value=0.4,
                                step=0.01
                                ),
                dbc.Row([
                                html.Label('Social distancing set up :',
                                style=style_title_slider),
                            ]),
                            dbc.Row(
                                html.P("First day of the social distancing.",
                                style=style_slider_text),
                            ),
                            html.P(id='Value_jour_dist',style=style_slider_value),
                            dcc.Slider(
                                id='Dist_jour_slide',
                                min=1,
                                max = 365,
                                value=100,
                                step=1
                                ),
            ],width=4),
            ],style ={
                'margin-right':'2em'
            })]

#FIGURE SLIDE COMPARAIRAISON

layout = html.Div([
    sidebar.sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'25em'}),
                html.H4('CORONAVIRUS SIMULATOR (FRENCH POPULATION)',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px','color':'rgb(87, 88, 90)','font-weight':'bolder'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('Simulator'),html.Div(className='encoche',style={'top':'52px','margin-top':'0px'})],href ='/simulation',className = "sousOngletActived")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.Div(
                                    [
                                        html.P('This COVID-19 simulator is based on the SEIR model. You can move every variables to see thir impact on the population.'),
                                        html.P('The initial value we choose are extracted from several past studies. Because of the simplicity of the model, the number may be exagerated but the purpose is to play with the model and observe the variation. For example, when the social distance rate is near 0%, there is less fatality.'),
                                        html.P('Do not be selfish, STAY HOME STAY SAFE !'),
                                        html.H6('Sources :'),
                                        html.Ul(
                                            [
                                                html.Li(
                                                    [html.A("SEIR Model",href='https://www.idmod.org/docs/hiv/model-seir.html')],
                                                ),
                                                html.Li(
                                                    [html.A("Variables",href='https://www.college-de-france.fr/media/philippe-sansonetti/UPL1414529259917354829_Covid_19_Sansonetti.pdf')],
                                                ),
                                            ]
                                        )
                                    ],style={'color':'white','width':'200px',"text-align":"justify"}
                                )
                            ],style={
                                'margin-top':'4em',
                                'margin-left':'1em',
                                'font-size': '15px'
                            }
                        ),
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row("dada",style={'color':'white','margin-left':'2em','margin-top':'1em'}),
                    html.Div(sim,style={'height':'850px'})
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])

#CALLBACKS
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
            'name':'Death',"hoverinfo": "none",'marker':{'color':'rgba(56, 108, 176,0.6)'}},
            {'x':sim.Idx.unique(),'y':sim[sim.Type == 'Hospital'].Nb,'type':'bar',
            'width':'0.7',
            'name':'Hospitalisation',"hoverinfo": "none",'marker':{'color':'rgba(141, 160, 203,0.6)'}},
            {'x':sim.Idx.unique(),'y':sim[sim.Type == 'I'].Nb,'type':'bar',
            'width':'0.7',
            'name':'Infected',"hoverinfo": "none",'marker':{'color':'rgba(237, 2, 128, 0.6)'}},
            {'x':sim.Idx.unique(),'y':sim[sim.Type == 'E'].Nb,'type':'bar',
            'width':'0.7',
            'name':'Exposed',"hoverinfo": "none",'marker':{'color':'rgba(253, 192, 134, 0.6)'}},
            
        ],
        'layout':{
            'barmode':'stack',
            'xaxis':{'type':'category',
            'dtick':'20'},
            'font':{
                'family':'Montserrat',
                'size':'15',
                'color':'rgb(87, 88, 90)'
            },
            'annotations':[{
                'x':dist_jour,
                'y':sim[sim.Type == 'I'].Nb.max()+sim[sim.Type == 'Hospital'].Nb.max()+sim[sim.Type == 'E'].Nb.max()+sim[sim.Type == 'Death'].Nb.max(),
                'text':'Start of the containment : R0 = {}'.format(round(R0*rho,2))
            },
                {
                'x':sim.loc[sim[sim.Type == 'Death'].ne(0).idxmax()[0]].Idx,
                'y':sim[sim.Type == 'I'].Nb.max(),
                'text':'First death'
                }],
            'shapes':[{
                'type':'line',
                'x0':dist_jour,
                'x1':dist_jour,
                'xref':'x',
                'yref':'y',
                'y0':'0',
                'y1':sim[sim.Type == 'I'].Nb.max()+sim[sim.Type == 'Hospital'].Nb.max()+sim[sim.Type == 'E'].Nb.max()+sim[sim.Type == 'Death'].Nb.max(),
                'line':{
                    'color':'Dark',
                    'width':'1',
                    'dash':'dot'
                    }
                },
                {
                    'type':'line',
                    'x0':sim.loc[sim[sim.Type == 'Death'].ne(0).idxmax()[0]].Idx,
                    'x1':sim.loc[sim[sim.Type == 'Death'].ne(0).idxmax()[0]].Idx,
                    'xref':'x',
                    'yref':'y',
                    'y0':'0',
                    'y1':sim[sim.Type == 'I'].Nb.max(),
                    'line':{
                    'color':'Dark',
                    'width':'1',
                    'dash':'dot'
                    }
                }]
            
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
        return '{} days'.format(value)
    else:
        return '{} day'.format(value)
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
        return '{} days'.format(value)
    else:
        return '{} day'.format(value)
@app.callback(
    Output('Value_incub','children'),
    [Input('incub_time_slide','value')]
)
def update_incub_display(value):
    if value >1:
        return '{} days'.format(value)
    else:
        return '{} day'.format(value)
@app.callback(
    Output('Value_infected','children'),
    [Input('N_malade_slider','value')]
)
def update_infected_display(value):
    if value >1:
        return '{} infected'.format(value)
    else:
        return '{} infected'.format(value)
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
        return '{} days'.format(value)
    else:
        return '{} day'.format(value)
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
        return '{} days'.format(value)
    else:
        return '{} day'.format(value)
#right text display slider value and graph value

@app.callback(
    Output('NbJours','children'),
    [Input("Apercu","hoverData")]
)
def display_jour(hoverData):
    try:
        x = hoverData['points'][0]['x']
        if x == 1:
            return '1 day'
        else:
            return str(int(x)) + ' days'
    except:
        return '365 days'
# TOTAL
@app.callback(
    [Output('Total_Deces','children'),
    Output('Total_Hosp','children'),
    Output('Total_Recover','children'),
    Output('Total_Infect','children'),
    Output('Total_Expose','children'),
    Output('Total_Susceptible','children')],
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
def display_Nb_Total(hoverData,R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour):
    try:
        x = hoverData['points'][0]['x']
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        death = sim[(sim.Type == 'Death')].set_index('Idx')
        hosp = sim[(sim.Type == 'Hospital')].set_index('Idx')
        recov = sim[(sim.Type == 'Recovered')].set_index('Idx')
        infect = sim[(sim.Type == 'I')].set_index('Idx')
        expose = sim[(sim.Type == 'E')].set_index('Idx')
        sus = sim[(sim.Type == 'S')].set_index('Idx')
        return '{:,}'.format(int(death.iloc[int(x)].Nb)),'{:,}'.format(int(hosp.iloc[int(x)].Nb)),'{:,}'.format(int(recov.iloc[int(x)].Nb)),'{:,}'.format(int(infect.iloc[int(x)].Nb)),'{:,}'.format(int(expose.iloc[int(x)].Nb)),'{:,}'.format(int(sus.iloc[int(x)].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        death = sim[(sim.Type == 'Death')].set_index('Idx')
        hosp = sim[(sim.Type == 'Hospital')].set_index('Idx')
        recov = sim[(sim.Type == 'Recovered')].set_index('Idx')
        infect = sim[(sim.Type == 'I')].set_index('Idx')
        expose = sim[(sim.Type == 'E')].set_index('Idx')
        sus = sim[(sim.Type == 'S')].set_index('Idx')
        return '{:,}'.format(int(death.iloc[int(m)].Nb)),'{:,}'.format(int(hosp.iloc[int(m)].Nb)),'{:,}'.format(int(recov.iloc[int(m)].Nb)),'{:,}'.format(int(infect.iloc[int(m)].Nb)),'{:,}'.format(int(expose.iloc[int(m)].Nb)),'{:,}'.format(int(sus.iloc[int(m)].Nb))

## day

@app.callback(
    [Output('Day_suceptible','children'),
    Output('Day_expose','children'),
    Output('Day_infect','children'),
    Output('Day_recover','children'),
    Output('Day_hosp','children'),
    Output('Day_deces','children'),
    ],
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
        surv = sim[(sim.Type == 'S')].set_index('Idx')
        exp = sim[(sim.Type == 'E')].set_index('Idx')
        infec = sim[(sim.Type == 'I')].set_index('Idx')
        recov = sim[(sim.Type == 'Recovered')].set_index('Idx')
        hosp = sim[(sim.Type == 'Hospital')].set_index('Idx')
        death = sim[(sim.Type == 'Death')].set_index('Idx')
        return '{:,}'.format(int(surv.iloc[int(x)].Nb - surv.iloc[int(x)-1].Nb)),'{:,}'.format(int(exp.iloc[int(x)].Nb - exp.iloc[int(x)-1].Nb)),'{:,}'.format(int(infec.iloc[int(x)].Nb - infec.iloc[int(x)-1].Nb)),'{:,}'.format(int(recov.iloc[int(x)].Nb - recov.iloc[int(x)-1].Nb)),'{:,}'.format(int(hosp.iloc[int(x)].Nb - hosp.iloc[int(x)-1].Nb)),'{:,}'.format(int(death.iloc[int(x)].Nb - death.iloc[int(x)-1].Nb))
    except:
        sim = simulator(R0,incub_time,infec_time,exposed,death_rate,death_time,p_severe,duree_hosp,rho,dist_jour)
        m = sim.Idx.max()
        surv= sim[(sim.Type == 'S')].set_index('Idx')
        exp = sim[(sim.Type == 'E')].set_index('Idx')
        infec = sim[(sim.Type == 'I')].set_index('Idx')
        recov = sim[(sim.Type == 'Recovered')].set_index('Idx')
        hosp = sim[(sim.Type == 'Hospital')].set_index('Idx')
        death = sim[(sim.Type == 'Death')].set_index('Idx')
        return '{:,}'.format(int(surv.iloc[int(m)].Nb - surv.iloc[int(m)-1].Nb)),'{:,}'.format(int(exp.iloc[int(m)].Nb - exp.iloc[int(m)-1].Nb)),'{:,}'.format(int(infec.iloc[int(m)].Nb - infec.iloc[int(m)-1].Nb)),'{:,}'.format(int(recov.iloc[int(m)].Nb - recov.iloc[int(m)-1].Nb)),'{:,}'.format(int(hosp.iloc[int(m)].Nb - hosp.iloc[int(m)-1].Nb)),'{:,}'.format(int(death.iloc[int(m)].Nb - death.iloc[int(m)-1].Nb))
