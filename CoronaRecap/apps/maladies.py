import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.express as px
from app import app
from apps import sidebar

#dataLoad
df = pd.read_csv('data/World Infectious Diseases.csv')
df['Diseases'] = 'Infectious Diseases'


#FIGURE SLIDE COMPARAIRAISON
fig1 = px.treemap(df, path=['Diseases', 'Epidemic','InfectiousDiseases'], values='ann_total_cases',
                  color = np.log10(df["CFR"]), hover_data=['R0'],
                  color_continuous_scale='RdBu', range_color=[-4,0],
                  color_continuous_midpoint=np.average(df['CFR']))
fig1.update_layout(
    font=dict(
            family='Montserrat',
            size=15,
            color='rgb(87, 88, 90)'
            ),
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=3,
        ticks='outside'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        showline=False,
        showticklabels=True,
    ),
    showlegend=True,
    plot_bgcolor='white'
)
fig1.update_layout(
    coloraxis_colorbar=dict(
    title="CFR",
    tickvals = np.arange(-4, 1),
    ticktext = np.around(np.exp(np.arange(-4, 1)),2)
    ),
    annotations=[
        dict(
            x=0.5,
            y=-0.15,
            showarrow=False,
            text="<a href='https://en.wikipedia.org/wiki/Basic_reproduction_number'>R<sub>0</sub>: Basic Reproductive Ratio</a> <br> <a href='https://en.wikipedia.org/wiki/Case_fatality_rate'> CFR: Case Fatality Rate </a>",
            xref="paper",
            yref="paper"
        )],
    autosize=True,
    margin=dict(
        b=100
    ),
    xaxis=dict(
        autorange=False,
        range=[-0.05674507980728292, -0.0527310420933204],
        type="linear"
    )
)
fig2 = px.treemap(df, path=['Diseases', 'Epidemic','InfectiousDiseases'], values='ann_total_fatalities',
                  color = np.log10(df["CFR"]), hover_data=['R0'],
                  color_continuous_scale='RdBu', range_color=[-4,0],
                  color_continuous_midpoint=np.average(df['CFR']))
fig2.update_layout(
    font=dict(
            family='Montserrat',
            size=15,
            color='rgb(87, 88, 90)'
            ),
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=3,
        ticks='outside'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        showline=False,
        showticklabels=True,
    ),
    showlegend=True,
    plot_bgcolor='white'
)
fig2.update_layout(coloraxis_colorbar=dict(
    title="CFR",
    tickvals = np.arange(-4, 1),
    ticktext = np.around(np.exp(np.arange(-4, 1)),2),
))
fig2.update_layout(
    annotations=[
        dict(
            x=0.5,
            y=-0.15,
            showarrow=False,
            text="<a href='https://en.wikipedia.org/wiki/Basic_reproduction_number'>R<sub>0</sub>: Basic Reproductive Ratio</a> <br> <a href='https://en.wikipedia.org/wiki/Case_fatality_rate'> CFR: Case Fatality Rate </a>",
            xref="paper",
            yref="paper"
        )],
    autosize=True,
    margin=dict(
        b=100
    ),
    xaxis=dict(
        autorange=False,
        range=[-0.05674507980728292, -0.0527310420933204],
        type="linear"
    )
)
layout = html.Div([
    sidebar.sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'25em'}),
                html.H4('DISEASES',id='titleMaladie',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px','color':'rgb(87, 88, 90)','font-weight':'bolder'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('Comparison diseases'),html.Div(className='encoche',style={'top':'53px','margin-top':'0px'})],href ='/maladies',className = "sousOngletActived")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Historical Epidemics')],href ='/maladies/historical',className = "sousOnglet")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Evolution')],href ='/maladies/evolution',className = "sousOnglet")
                            ]
                        ),
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row(
                        [
                            html.Button('Cases',id='BtnFigureDoubleGraph1',className='btnChoixActive',n_clicks=1),
                            html.Button('Fatality',id='BtnFigureDoubleGraph2',className='btnChoixNonActive',n_clicks=0),
                        ],className='justify-content-end',style={
                            'margin-right':'8em',
                            'margin-top':'2em'
                        }
                    ),
                    html.Div("CFR (case fatality rate): The proportion of deaths from a certain disease compared to the total number of people diagnosed with the disease for a certain period of time.",
                    style={
                        'font-size':'15px',
                        'margin-top':'2em',
                        'font-style':'italic',
                        'margin-left':'5.6em',
                        'color':'#404040'
                    }),
                    html.Div("R0 (basic reproductive ratio): Can be considered as the expected number of cases directly generated by one case in a population where all individuals are susceptible to infection.",
                    style={
                        'font-size':'15px',
                        'margin-top':'2em',
                        'font-style':'italic',
                        'margin-left':'5.6em',
                        'color':'#404040'
                    }),
                    dcc.Loading(
                        dcc.Graph(id='doubleGraph',style={'height':'800px'}),
                        type='circle'
                    )
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])




#CALLBACKS
@app.callback(
    [Output('doubleGraph','figure'),
    Output('titleMaladie','children')],
    [Input('BtnFigureDoubleGraph1','className')]
)
def show_graph(className,fig1=fig1,fig2=fig2):
    if className == 'btnChoixActive':
        return fig1,'Comparison of Differents Infectious Diseases (Annual total cases)'
    else:
        return fig2,'Comparison of Differents Infectious Diseases (Annual total fatalities)'


@app.callback(
    [Output('BtnFigureDoubleGraph1','className'),
    Output('BtnFigureDoubleGraph2','className')],
    [Input('BtnFigureDoubleGraph1','n_clicks'),
    Input('BtnFigureDoubleGraph2','n_clicks')
    ]
)
def change_color(n_clicks1,n_clicks2):
    if n_clicks1 > n_clicks2:
        return 'btnChoixActive','btnChoixNonActive'
    else:
        return 'btnChoixNonActive','btnChoixActive'
#Callback menu déroulant
@app.callback(
    [Output('mySidebar','style'),
    Output('btnOpen','style')],
    [Input('btnOpen','n_clicks')]
)
def show_side_bar(n_clicks):
    if n_clicks is not None:
        if (n_clicks % 2) != 0:
            return  {
                'width':'0px'
            },{
                'margin-left':'0px'
            }
        else:
            return {
                'width':'350px'
            },{
                'margin-left':'350px',
            }
    elif n_clicks == 'None':
        return {
                'width':'0px'
            },{
                'margin-left':'0px'
            }