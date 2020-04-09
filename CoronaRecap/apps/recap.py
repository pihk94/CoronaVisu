import dash
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.express as px
from app import app
from apps import GetData
from apps import graph 
import plotly.graph_objects as go
import time
#dataLoad
df  =GetData.get_world('confirmed')

#FCT 
def make_bars(country,df = df):
    
    t =df[(df['Country/Region'] == country)].groupby('Country/Region').sum()
    lst=  [list(t[col].values)[0] for col in t.columns if col not in ['Continent','Country/Region','Province/State','Lat','Long']]
    variation = [lst[i] -  lst[i-1] for i in range(1,len(lst))]
    color = {
        '0':{
            'border-right':'1px solid rgba(255,255,255,0.5)',
            'width':'3px',
        },
        '1-10':{
            'background':'rgba(255, 152, 0, 0.1)',
            'border-right':'1px solid rgba(255,255,255,0.5)',
            'width':'3px',
        },
        '10-100':{
            'background':'rgba(255, 152, 0, 0.4)',
            'border-right':'1px solid rgba(255,255,255,0.5)',
            'width':'3px',
        },
        '100-1000':{
            'background':'rgba(255, 152, 0, 0.7)',
            'border-right':'1px solid rgba(255,255,255,0.5)',
            'width':'3px',
        },
        '+1000':{
            'background':'rgba(255, 152, 0, 1)',
            'border-right':'1px solid rgba(255,255,255,0.5)',
            'width':'3px',
        },
        
    }
    render = []
    for val in variation:
        if val == 0:
            render.append(html.Div(style=color['0']))
        elif val >0 and val <10:
            render.append(html.Div(style=color['1-10']))
        elif val>= 10 and val < 100:
            render.append(html.Div(style=color['10-100']))
        elif val >=100 and val <1000:
            render.append(html.Div(style=color['100-1000']))
        elif val >=1000:
            render.append(html.Div(style=color['+1000']))
    return html.Div(render,className='d-flex',style={'height':'15px'})
CSS =  {
    'danger':{
        'font-size':'15px',
        'color':'#cc1100',
        'font-weight':'bolder'
    },
    'important':{
        'font-size':'15px',
        'font-weight':'bold'
    }
}

#recap
recap = [
    dbc.Container(
        [
        dcc.DatePickerRange(
        id='my-date-picker-range',
        minimum_nights=2,
        with_portal=True,
        min_date_allowed=datetime(2020, 1, 22),
        max_date_allowed=datetime.now() - timedelta(1),
        initial_visible_month=datetime(2020, 4, 1),
        start_date=datetime.now() - timedelta(6),
        end_date=datetime.now() - timedelta(1),
        display_format='D-M-Y',
        style={"display":"None"}
        ),
        dcc.Loading([  
            dbc.Row(html.Span(id='Maj_date',style={'text-transform':'uppercase','font-size':'9px'}),className='justify-content-center'),
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                        html.Span('Cas confirmé')
                    ),
                    dbc.Row(
                        html.Span(id='Total_confirm_case',children ='',style=CSS['important'])
                    ),
                    dbc.Row(
                        html.Span(id = 'Var_confirm',children = '',style=CSS['danger'])
                    )
                ],width = 4),
                dbc.Col([
                    dbc.Row(
                        html.Span('Décès')
                    ),
                    dbc.Row(
                        html.Span(id='Total_death',children = '',style=CSS['important'])
                    ),
                    dbc.Row(
                        html.Span(id='Var_death',children='',style=CSS['danger'])
                    )
                ],width = 4),
                dbc.Col([
                    dbc.Row(
                        html.Span('Rétabli')
                    ),
                    dbc.Row(
                        html.Span(id='Total_recov',children = '',style=CSS['important'])
                    ),
                    dbc.Row(
                        html.Span(id='Var_recov',children='',style=CSS['danger'])
                    )
                ],width = 4),
            ],
            style={
                'background':'#f8f9fa',
                'padding-left': '10em'
                }),
            dbc.Row(
                [
                    html.P([
                        'Dans les ',
                        html.Span(id='NbreJours',children ='',style={'font-weight':'bold'}),
                        ' derniers jours, ',
                        html.Span(id='NbreCasNew',children ='',style={'font-weight':'bold'}),
                        '  nouveaux cas de Coronavirus ont été reporté à travers le monde. Parmis ceux-là ',
                        html.Span(id='NbreCasNewFr',children ='',style={'font-weight':'bold'}),
                        ' viennent de France.',
                    ])
                    
                ],className='justify-content-center'
            ),
            dbc.Row(html.H4(children = 'CAS',style={'font-weight':'bold'}),className='justify-content-center'),
            dbc.Row(
                [
                    dbc.Col([
                        dbc.Row(
                            html.Span('Chine')
                        ),
                        dbc.Row(
                            html.Span(id='chine_cas',style=CSS['important'])
                        ),
                        dbc.Row(
                            html.Span(id='chine_delta',style=CSS['danger'])
                        )
                    ]),
                    dbc.Col([
                        dbc.Row(
                            html.Span('Italie')
                        ),
                        dbc.Row(
                            html.Span(id='italy_cas',style=CSS['important'])
                        ),
                        dbc.Row(
                            html.Span(id='italy_delta',style=CSS['danger'])
                        )
                    ]),
                    dbc.Col([
                        dbc.Row(
                            html.Span('Allemagne')
                        ),
                        dbc.Row(
                            html.Span(id='allemagne_cas',style=CSS['important'])
                        ),
                        dbc.Row(
                            html.Span(id='allemagne_delta',style=CSS['danger'])
                        )
                    ]),
                    dbc.Col([
                        dbc.Row(
                            html.Span('Espagne')
                        ),
                        dbc.Row(
                            html.Span(id='spain_cas',style=CSS['important'])
                        ),
                        dbc.Row(
                            html.Span(id='spain_delta',style=CSS['danger'])
                        )
                    ]),
                    dbc.Col([
                        dbc.Row(
                            html.Span('Etats-Unis')
                        ),
                        dbc.Row(
                            html.Span(id='us_cas',style=CSS['important'])
                        ),
                        dbc.Row(
                            html.Span(id='us_delta',style=CSS['danger'])
                        )
                    ]),
                    dbc.Col([
                        dbc.Row(
                            html.Span('France')
                        ),
                        dbc.Row(
                            html.Span(id='fr_cas',style=CSS['important'])
                        ),
                        dbc.Row(
                            html.Span(id='fr_delta',style=CSS['danger'])
                        )
                    ]),
                ],
            style={
                'background':'#f8f9fa',
                'padding-left': '6em'
                }
            ),
        html.Table(id='recap',style = {
            'margin-top':'2em',
            'margin-left':'5em'
        })
        ],type='default'),
    ])
]
    


sidebar = html.Div(id='mySidebar',className ="sidebar",children=[
            html.A(href='/',children = [html.Img(src='assets/png/home.png',style={'width':'32px','height':'32px','margin-left':'3.6em'}),html.Div('Home',style={
                'font-size':'14px',
                'text-align':'center'
            })],style={'background-color':'#036'}),
            html.A(href='#',children='Récapitulatif',style={'text-align':'left'}),
            html.A(href='#',children='Autres épidémies',style={'text-align':'left'}),
            html.A(href='#',children='Finance',style={'text-align':'left'}),
            html.A(href='#',children='GoogleTrend',style={'text-align':'left'}),
        ])

layout = html.Div([
    sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'50em'}),
                html.H4('COVID-19 OVERVIEW',id='titleMaladie',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('Overview'),html.Div(className='encoche',style={'top':'36px','margin-top':'0px'})],href ='/recap',className = "sousOngletActived")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('World Trend')],href ='/recap/world',className = "sousOnglet")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Continental Trend')],href ='/recap/continent',className = "sousOnglet")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Country Trend')],href ='/recap/country',className = "sousOnglet")
                            ]
                        ),
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row("dada",style={'color':'white','margin-left':'2em','margin-top':'1em'}),
                    html.Div(
                        recap
                    )
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])

@app.callback(
    [Output('Total_confirm_case','children'),
    Output('Var_confirm','children'),
    Output('Total_death','children'),
    Output('Var_death','children'),
    Output('Total_recov','children'),
    Output('Var_recov','children'),
    Output('Maj_date','children'),
    Output('NbreJours','children'),
    Output('NbreCasNew','children'),
    Output('NbreCasNewFr','children'),
    Output('chine_cas','children'),
    Output('chine_delta','children'),
    Output('italy_cas','children'),
    Output('italy_delta','children'),
    Output('allemagne_cas','children'),
    Output('allemagne_delta','children'),
    Output('spain_cas','children'),
    Output('spain_delta','children'),
    Output('us_cas','children'),
    Output('us_delta','children'),
    Output('fr_cas','children'),
    Output('fr_delta','children')],
    [Input('my-date-picker-range','end_date'),
    Input('my-date-picker-range','start_date')]
)
def recap_world(dt,previous):
    previous = (pd.to_datetime(dt,dayfirst=True)-pd.to_datetime(previous,dayfirst=True)).days
    if dt == time.strftime('%d/%m/%Y'):
        dt = (datetime.now() - timedelta(1)).strftime('%d/%m/%Y')
    df_recap=GetData.get_recap_by_country(dt,previous=int(previous))
    df_confirmed=GetData.get_world('confirmed')
    confirmed=df_confirmed.iloc[:,-1].sum()
    confirmedp=df_recap['Cases (+)'].sum(axis=0)
    df_deaths=GetData.get_world('deaths')
    deaths=df_deaths.iloc[:,-1].sum()
    deathsp=df_recap['Deaths (+)'].sum(axis=0)
    df_recovered=GetData.get_world('recovered')
    recovered=df_recovered.iloc[:,-1].sum()
    recoveredp=df_recap['Recovered (+)'].sum(axis=0)
    france_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="France"]):,}'
    france_casesp2="{0}".format(france_casesp)
    us_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="US"]):,}'
    us_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="US"]):,}'
    france_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="France"]):,}'
    italy_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="Italy"]):,}'
    italy_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="Italy"]):,}'
    germany_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="Germany"]):,}'
    germany_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="Germany"]):,}'
    china_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="China"]):,}'
    china_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="China"]):,}'
    spain_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="Spain"]):,}'
    spain_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="Spain"]):,}'
    return '{:,}'.format(confirmed),'(+ {:,})'.format(confirmedp),'{:,}'.format(deaths),'(+ {:,})'.format(deathsp),'{:,}'.format(recovered),'(+ {:,})'.format(recoveredp),\
        'Mise à jour le {} (+ Variations sur les {} derniers jours)'.format(pd.to_datetime(dt).strftime('%d/%m/%Y'),previous),'{:,}'.format(previous),'{:,}'.format(recoveredp),'{}'.format(france_casesp2),\
            '{}'.format(china_cases),'(+ {})'.format(china_casesp),'{}'.format(italy_cases),'(+ {})'.format(italy_casesp),'{}'.format(germany_cases),'(+ {})'.format(germany_casesp),\
                '{}'.format(spain_cases),'(+ {})'.format(spain_casesp),'{}'.format(us_cases),'(+ {})'.format(us_casesp),'{}'.format(france_cases),'(+ {})'.format(france_casesp2)
@app.callback(
    Output('recap','children'),
    [Input('my-date-picker-range','end_date'),
    Input('my-date-picker-range','start_date')]
)
def recap_table(dt,previous):
    previous = (pd.to_datetime(dt,dayfirst=True)-pd.to_datetime(previous,dayfirst=True)).days
    df_recap=GetData.get_recap_by_country(dt,previous=previous)
    columns = ['Pays','Nouveaux Cas','Total des cas','Total décès','Nouveau décès','Mortalité','Rétabli']
    df_H5=pd.DataFrame(columns=columns)
    df_H5["Pays"]=x = ['{0}'.format(i) for i in df_recap["Country/Region"]]
    df_H5["Total des cas"]=df_recap["Cases"]
    df_H5["Total décès"]=df_recap["Deaths"]
    df_H5["Mortalité"]=df_H5["Total décès"]/df_H5["Total des cas"]
    df_H5["Total décès"]=df_recap["Deaths"]
    df_H5["Rétabli"]=df_recap["Recovered"]
    df_H5["Nouveaux cas"]=[f'{i:,}'for i in df_recap["Cases (+)"]]
    df_H5["Nouveaux cas"]=["(+{0})".format(str(i)) for i in df_H5["Nouveaux cas"]]
    df_H5["Nouveau décès"]=[f'{i:,}'for i in df_recap['Deaths (+)']]
    df_H5["Nouveau décès"]=["(+{0})".format(str(i)) for i in df_H5["Nouveau décès"]]
    df_H5["Mortalité"]=["{:.2%}".format(i) for i in df_H5["Mortalité"]]
    df_H5["Rétabli"]=[f'{i:,}'for i in df_H5["Rétabli"]]
    df_H5["Total des cas"]=[f'{i:,}'for i in df_H5["Total des cas"]]
    df_H5["Total décès"]=[f'{i:,}'for i in df_H5["Total décès"]]
    rows =[]
    for index,row in df_H5.iterrows():
        rows.append(html.Tr([html.Td(row.Pays,style={'font-weight':'bold','text-align':'right'}),html.Td(make_bars(row.Pays),style={'vertical-align':'middle'}),
        html.Td(row['Total des cas'],style={'font-weight':'bolder'}),html.Td(row['Nouveaux cas'],style = CSS['danger']),html.Td(row['Total décès']),html.Td(row['Nouveau décès'],style = CSS['danger']),html.Td(row['Mortalité']),html.Td(row['Rétabli'])],style={
            'border-bottom':'1px solid #e8e8e8'
        }))
    return [
        html.Thead([
            html.Tr(
                [
                    html.Th(children=''
                        ,style ={
                            'width':'150px'
                        }
                    ),
                    html.Th(
                        [
                            html.Div(children='10',
                            style={
                                "width":"27px",
                                "height":"15px",
                                "font-size":"8px"
                            }),
                            html.Div(children='100',
                            style={
                                "width":"27px",
                                "height":"15px",
                                "font-size":"8px"
                            }),
                            html.Div(children='1000',
                            style={
                                "width":"27px",
                                "height":"15px",
                                "font-size":"8px"
                            }),
                        ]
                        ,style ={
                            'width':'170px',
                            "height":"15px",
                            'vertical-align':'middle',
                            "display":"flex",
                            "margin-left":"85px"
                        }
                    ),
                    html.Th()
                ]
            ),
            html.Tr(
                [
                    html.Th(children=''
                        ,style ={
                            'width':'150px'
                        }
                    ),
                    html.Th(
                        [
                            html.Div(children='',
                            style={
                                "background": "rgba(255, 152, 0,0.1)",
                                "width":"27px",
                                "height":"15px"
                            }),
                            html.Div(children='',
                            style={
                                "background": "rgba(255, 152, 0,0.4)",
                                "width":"27px",
                                "height":"15px"
                            }),
                            html.Div(children='',
                            style={
                                "background": "rgba(255, 152, 0,0.7)",
                                "width":"27px",
                                "height":"15px"
                            }),
                            html.Div(children='',
                            style={
                                "background": "rgba(255, 152, 1)",
                                "width":"27px",
                                "height":"15px"
                            }),
                        ]
                        ,style ={
                            'width':'170px',
                            "height":"15px",
                            'vertical-align':'middle',
                            "display":"flex",
                            "margin-left":"50px"
                        }
                    ),
                    html.Th()
                ]
            ),
            html.Tr(
                [
                    html.Th(
                    'Pays',style={'text-align':'right','width':'180px'}
                    ),
                    html.Th(
                    'Evolution des cas',style={'text-align':'center','width':'170px'}
                    ),
                    html.Th(
                        'Total des cas',style ={
                            'text-align':'center',
                            'width':'250px'
                        }
                    ),
                    html.Th(
                        'Nouveaux cas',style={
                            'text-align':'center',
                            'width':'250px'
                        }
                    ),
                    html.Th(
                        'Total décès',style={
                            'text-align':'center',
                            'width':'250px'
                        }
                    ),
                    html.Th(
                        'Nouveaux décès',style={
                            'text-align':'center',
                            'width':'300px'
                        }
                    ),
                    html.Th(
                        'Mortalité',style={
                            'text-align':'center',
                            'width':'200px'
                        }
                    ),
                    html.Th(
                        'Rétablis',style={
                            'text-align':'center',
                            'width':'200px'
                        }
                    )
                ],
                style = {
                    'border-bottom': '2px solid',
                    'text-transform':'uppercase',
                    "font-size":"14px"
                }
            )
        ]),
        html.Tbody(
            [html.Tr([html.Td(),html.Td([html.Div('22 Janvier'),html.Div("Aujourd'hui")],style = {'display':'flex','justify-content':'space-between','font-size':'9px'}),html.Td(),html.Td('( + NOUVEAU ) depuis le {}'.format((pd.to_datetime(dt,dayfirst=True) - timedelta(previous)).strftime('%d/%m/%Y')),style={"font-size": "9px",'color':'#999','text-align':'left'}),html.Td(),html.Td()])]+
            rows
        )
    ]









#CALLBACKS
# @app.callback(
#     [Output('doubleGraph','figure'),
#     Output('titleMaladie','children')],
#     [Input('BtnFigureDoubleGraph1','className')]
# )
# def show_graph(className,fig1=fig1,fig2=fig2):
#     if className == 'btnChoixActive':
#         return fig1,'Comparison of Differents Infectious Diseases (Annual total cases)'
#     else:
#         return fig2,'Comparison of Differents Infectious Diseases (Annual total fatalities)'


# @app.callback(
#     [Output('BtnFigureDoubleGraph1','className'),
#     Output('BtnFigureDoubleGraph2','className')],
#     [Input('BtnFigureDoubleGraph1','n_clicks'),
#     Input('BtnFigureDoubleGraph2','n_clicks')
#     ]
# )
# def change_color(n_clicks1,n_clicks2):
#     if n_clicks1 > n_clicks2:
#         return 'btnChoixActive','btnChoixNonActive'
#     else:
#         return 'btnChoixNonActive','btnChoixActive'
