import dash
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
def SEIR_mano(val_init,coeff,t,N=6000):
    """
        Input : 
            val_init : Liste de 4 valeurs initials que va prendre le modèle 
            coeff : Liste de valeurs pour Alpha,Gamma, Beta et Rho
            t :
        Output:
            
    """
    S0,E0,I0,R0= val_init
    S,E,I,R = [S0],[E0],[I0],[R0]
    a,b,g,r=coeff
    dt = t[1]-t[0]
    for _ in t[1:]:
        nS = S[-1] - (r*b*S[-1]*I[-1]/N)*dt
        nE = E[-1] + (r*b*S[-1]*I[-1]/N-a*E[-1])*dt
        nI = I[-1] + (a*E[-1]-g*I[-1])*dt
        nR = R[-1] + (g*I[-1])*dt
        S.append(nS)
        E.append(nE)
        I.append(nI)
        R.append(nR)
    return np.stack([S,E,I,R]).T
def simulator(R0,incub_time,infec_time,exposed,N=600,rho =1,t = range(0,100)):
    alpha = 1/incub_time
    gamma = 1/infec_time
    beta = R0 * gamma
    rho = 1
    N = 6000
    coeff = alpha, beta,gamma,rho
    init_vals = N-exposed,exposed,0,0
    df = pd.DataFrame(SEIR_mano(init_vals,coeff,t),columns=['S','E','I','R'])
    lst=[]
    for index,row in df.iterrows():
        lst+=[(round(row.S),'S',index)]
        lst+=[(round(row.E),'E',index)]
        lst+=[(round(row.I),'I',index)]
        lst+=[(round(row.R),'R',index)]
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
        ],width=8),
        dbc.Col([
            
        ],width = 4)
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
                        html.P("Le nombre moyen d'individus qu'une personne infectieuse pourra infecter, tant qu'elle sera contagieuse.",
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
        dbc.Col(width = 6)
    ])
])

@app.callback(
    Output('Apercu','figure'),
    [Input('R0_slider','value'),
    Input('incub_time_slide','value'),
    Input('infect_time_slide','value'),
    Input('N_malade_slider','value')]
)
def update_figure(R0,incub_time,infec_time,exposed):
    sim = simulator(R0,incub_time,infec_time,exposed)
    return  {
        'data' :[
            {'x':sim.Idx,'y':sim[sim.Type == 'I'].Nb,'type':'bar',
            'width':'0.3',
            'name':'Infectieux','marker':{'color':'rgba(237, 2, 128, 0.6)'}},
            {'x':sim.Idx,'y':sim[sim.Type == 'E'].Nb,'type':'bar',
            'width':'0.3',
            'name':'Exposé','marker':{'color':'rgba(253, 192, 134, 0.6)'}},
        ],
        'layout':{
            'barmode':'stack',
            'xaxis':{'type':'category'}
        }
    }
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
if __name__ == '__main__':
    app.run_server(debug=True)