import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from apps import GetData
from apps import graph 
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd 
import plotly.graph_objects as go

from app import app


navbar = dbc.Navbar(
        [
        html.A(
            dbc.Row(
            [
                dbc.Col(html.Img(src= app.get_asset_url('png/008-virus.png'),height='32px',width ='32px')),
                dbc.Col(dbc.NavbarBrand('CoronaRecap',className="ml-2"))
            ],
                align="center",
                no_gutters=True,
                ),
                href="/"),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Récapitulatif",href="/")),
                    dbc.NavItem(dbc.NavLink("Simulateur",href="/simulation")),
                ],className="ml-auto",navbar=True
            )
            
        ],
    color="dark",
    dark=True,
)


df=GetData.get_recap_by_country("20/03/2020",10)


style_H1 ={"display": "block",
            "margin-left": "auto",
            "margin-right": "auto",'textAlign': 'center'}

style_label = {"display": "block",
            "margin-left": "auto",
            "margin-right": "auto",'textAlign': 'center', 'color':'black'}

style_phraseH5 = {'color': 'black', 'textAlign': 'center',\
               'margin-bottom':'0px','margin-top': '0px'  }

style_fig_H2={
            'height': 152,
            'width': 500,
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto",
            }

phrase_label='Updated on **{0}** (+Change since **{1}** days ago.)'\
            .format(graph.date,graph.previous)
            
phrase_H3="In the last **{0}** days, **{1}** new Coronavirus cases have been \
    reported worldwide. Of which **{2}** are from France.".format(\
    graph.previous, graph.confirmedp, graph.france_casesp2)
 
phrase_H4="In the last **{0}** days, **{1}** new Coronavirus deaths have been \
    reported worldwide. Of which **{2}** are from France.".format(\
    graph.previous, graph.deathsp, graph.france_deathsp2)
#############################################################################

day=["17/03/2020","18/03/2020","19/03/2020","20/03/2020"]   
previous=np.linspace(5,50,10)
layout = html.Div(children=[
    navbar,
    html.H1(children='Tracking the spread of the Coronavirus', \
            style=style_H1),
            
    dcc.Input(
    id='inputdate',
    value="20/03/2020",
    type='text'
    ),

    dcc.Input(
    id='inputprevious',    
    value=5,
    type='number'
    ),

    dcc.Graph(id="outputfigure1", 
              style=style_fig_H2
              ),

    dcc.Markdown(id="outputlabel1"\
            ,style=style_label), 
               
    dcc.Graph(id="outputfigure2"),
    
    dcc.Markdown(id="outputlabel2" \
            ,style=style_label)
 
    ,dcc.Graph(id="outputfigure3"),
    
    dcc.Markdown(id="outputlabel3" \
            ,style=style_label)
    
    ,dcc.Graph(id="outputfigure4"),

])
    
@app.callback(
    dash.dependencies.Output('outputlabel1', 'children'),
   [dash.dependencies.Input('inputdate', 'value'), 
    dash.dependencies.Input('inputprevious', 'value')])
def updatelabel1(valued,valuep):

    return 'Updated on **{0}** (+Change since **{1}** days ago.)'\
            .format(valued,valuep)

@app.callback(
    dash.dependencies.Output('outputlabel2', 'children'),
   [dash.dependencies.Input('inputdate', 'value'), 
    dash.dependencies.Input('inputprevious', 'value')])
def updatelabel2(valued,valuep):
    
    previous=int(valuep)
    date=valued
    df_recap=GetData.get_recap_by_country(date,previous=previous)
    
    #Récupération des cas confirmés

    confirmedp=df_recap['Cases (+)'].sum(axis=0)
    france_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="France"]):,}'
    france_casesp2="{0}".format(france_casesp)  
    
    return "In the last **{0}** days, **{1}** new Coronavirus cases have been \
    reported worldwide. Of which **{2}** are from France.".format(\
    valuep, confirmedp, france_casesp2)
    
@app.callback(
    dash.dependencies.Output('outputlabel3', 'children'),
   [dash.dependencies.Input('inputdate', 'value'), 
    dash.dependencies.Input('inputprevious', 'value')])
def updatelabel3(valued,valuep): 
    
    previous=int(valuep)
    date=valued
    df_recap=GetData.get_recap_by_country(date,previous=previous)

    deathsp=df_recap['Deaths (+)'].sum(axis=0)
    
    france_deathsp=f'{int(df_recap["Deaths (+)"][df_recap["Country/Region"]=="France"]):,}'
    france_deathsp2="{0}".format(france_deathsp)
    
    return "In the last **{0}** days, **{1}** new Coronavirus deaths have been \
    reported worldwide. Of which **{2}** are from France.".format(\
    previous, deathsp, france_deathsp2)   
    
@app.callback(
    dash.dependencies.Output('outputfigure1', 'figure'),
   [dash.dependencies.Input('inputdate', 'value'), 
    dash.dependencies.Input('inputprevious', 'value')])
def updatefigure1(valued,valuep):
    previous=int(valuep)
    date=valued
    df_recap=GetData.get_recap_by_country(date,previous=previous)
    
    #Récupération des cas confirmés
    df_confirmed=GetData.get_world('confirmed')
    confirmed=df_confirmed.iloc[:,5:].sum(axis=1).sum(axis=0)
    confirmedp=df_recap['Cases (+)'].sum(axis=0)
    #Récupération des cas morts
    df_deaths=GetData.get_world('deaths')
    deaths=df_deaths.iloc[:,5:].sum(axis=1).sum(axis=0)
    deathsp=df_recap['Deaths (+)'].sum(axis=0)
    #Récupération des cas guéris
    df_recovered=GetData.get_world('recovered')
    recovered=df_recovered.iloc[:,5:].sum(axis=1).sum(axis=0)
    recoveredp=df_recap['Recovered (+)'].sum(axis=0)   
    
    confirmed=f'{confirmed:,}'
    deaths=f'{deaths:,}'
    recovered=f'{recovered:,}'
    
    confirmedp=f'{confirmedp:,}'
    deathsp=f'{deathsp:,}'
    recoveredp=f'{recoveredp:,}'
    
    a="<b>{0}</b>".format(confirmed)
    b="<b>{0}</b>".format(deaths)
    c="<b>{0}</b>".format(recovered)
    
    e="<b>(+{0})</b>".format(confirmedp)
    f="<b>(+{0})</b>".format(deathsp)
    g="<b>(+{0})</b>".format(recoveredp)


    #CSS 
    fill_color_H2='lightgray'
    line_color_H2='lightgray'
    font_color_H2=[['black','red']]
    font_size_H2=[15]
    
    
    #layout = go.Layout( autosize=True, **margin={'l': 0, 'r': 0, 't': 20, 'b': 0}**)
    
    fig_H2= go.Figure(data=[go.Table(
      header=dict(values=["Confirmed Cases","Deaths", "Recovered"]
        ,
        line_color=line_color_H2,fill_color=fill_color_H2,
        align='center',font=dict(color='black', size=10)
      ),
      cells=dict(
        values=[[a,e],[b,f], [c,g]],align='center',
        line_color=line_color_H2,
        fill_color=fill_color_H2, font_color=font_color_H2, 
        font_size=font_size_H2
        
        ))
    ])
    fig_H2.update_layout(
        autosize=False,
        width=500,
        height=170,
        margin=dict(
            l=20,
            r=20,
            b=20,
            t=50,
            pad=10
        ),
        title_text="<b>WORLD</b>",title_x=0.5,
       title_font_color='black'
    )

    return fig_H2

@app.callback(
    dash.dependencies.Output('outputfigure2', 'figure'),
   [dash.dependencies.Input('inputdate', 'value'), 
    dash.dependencies.Input('inputprevious', 'value')])
def updatefigure2(valued,valuep):
    previous=int(valuep)
    date=valued
    df_recap=GetData.get_recap_by_country(date,previous=previous)
    
    fill_color_H2='lightgray'
    line_color_H2='lightgray'
    font_color_H2=[['black','red']]

    #USA  
    us_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="US"]):,}'
    us_cases="<b>{0}</b>".format(us_cases)
    
    us_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="US"]):,}'
    us_casesp="<b>(+{0})</b>".format(us_casesp)
    
    #France
    france_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="France"]):,}'
    france_cases="<b>{0}</b>".format(france_cases)
    
    france_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="France"]):,}'
    france_casesp="<b>(+{0})</b>".format(france_casesp)
    
    #Italy
    italy_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="Italy"]):,}'
    italy_cases="<b>{0}</b>".format(italy_cases)
    
    italy_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="Italy"]):,}'
    italy_casesp="<b>(+{0})</b>".format(italy_casesp)
    
    #Germany
    germany_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="Germany"]):,}'
    germany_cases="<b>{0}</b>".format(germany_cases)
    
    germany_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="Germany"]):,}'
    germany_casesp="<b>(+{0})</b>".format(germany_casesp)

    #China
    china_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="China"]):,}'
    china_cases="<b>{0}</b>".format(china_cases)
    
    china_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="China"]):,}'
    china_casesp="<b>(+{0})</b>".format(china_casesp)
    
    #Spain
    spain_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="Spain"]):,}'
    spain_cases="<b>{0}</b>".format(spain_cases)
    
    spain_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="Spain"]):,}'
    spain_casesp="<b>(+{0})</b>".format(spain_casesp)
    
    #Iran
    iran_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="Iran"]):,}'
    iran_cases="<b>{0}</b>".format(iran_cases)
    
    iran_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="Iran"]):,}'
    iran_casesp="<b>(+{0})</b>".format(iran_casesp)

    
    values_H3=[[china_cases,china_casesp],[france_cases,france_casesp],\
               [germany_cases,germany_casesp],[us_cases,us_casesp],\
               [spain_cases,spain_casesp], [iran_cases,iran_casesp],\
               [italy_cases,italy_casesp]]
    fig_H3= go.Figure(data=[go.Table(
      header=dict(values=["China","France", "Germany"\
                          ,"US","Spain","Iran"\
                          ,"Italy"]
        ,
        line_color=line_color_H2,fill_color=fill_color_H2,
        align='center',font=dict(color='black', size=10)
      ),
      cells=dict(
              line_color=line_color_H2,fill_color=fill_color_H2,font_color=font_color_H2,
        values=values_H3, font_size=13
        ))
    ])
    
    fig_H3.update_layout(
        autosize=False,
        width=1000,
        height=170,
        margin=dict(
            l=300,
            r=20,
            b=0,
            t=40,
            pad=20
        ),
        title_text="<b>CASES</b>",title_x=0.63,
       title_font_color='black'
    ) 
    return fig_H3

@app.callback(
    dash.dependencies.Output('outputfigure3', 'figure'),
   [dash.dependencies.Input('inputdate', 'value'), 
    dash.dependencies.Input('inputprevious', 'value')])
def updatefigure3(valued,valuep):
    previous=int(valuep)
    date=valued
    df_recap=GetData.get_recap_by_country(date,previous=previous)
    
    fill_color_H2='lightgray'
    line_color_H2='lightgray'
    font_color_H2=[['black','red']]

    #USA  
    us_deaths=f'{int(df_recap["Deaths"][df_recap["Country/Region"]=="US"]):,}'
    us_deaths="<b>{0}</b>".format(us_deaths)
    
    us_casesp=f'{int(df_recap["Cases (+)"][df_recap["Country/Region"]=="US"]):,}'
    us_deathsp=f'{int(df_recap["Deaths (+)"][df_recap["Country/Region"]=="US"]):,}'
    us_casesp="<b>(+{0})</b>".format(us_casesp)
    us_deathsp="<b>(+{0})</b>".format(us_deathsp)
    
    #France
    france_deaths=f'{int(df_recap["Deaths"][df_recap["Country/Region"]=="France"]):,}'
    france_deaths="<b>{0}</b>".format(france_deaths)   

    france_deathsp=f'{int(df_recap["Deaths (+)"][df_recap["Country/Region"]=="France"]):,}'
    france_deathsp="<b>(+{0})</b>".format(france_deathsp)
    
    #Italy
    italy_deaths=f'{int(df_recap["Deaths"][df_recap["Country/Region"]=="Italy"]):,}'
    italy_deaths="<b>{0}</b>".format(italy_deaths)
    
    italy_deathsp=f'{int(df_recap["Deaths (+)"][df_recap["Country/Region"]=="Italy"]):,}'
    italy_deathsp="<b>(+{0})</b>".format(italy_deathsp)
    
    #Germany
    germany_deaths=f'{int(df_recap["Deaths"][df_recap["Country/Region"]=="Germany"]):,}'
    germany_deaths="<b>{0}</b>".format(germany_deaths)
    
    germany_deathsp=f'{int(df_recap["Deaths (+)"][df_recap["Country/Region"]=="Germany"]):,}'
    germany_deathsp="<b>(+{0})</b>".format(germany_deathsp)
    
    #China
    china_deaths=f'{int(df_recap["Deaths"][df_recap["Country/Region"]=="China"]):,}'
    china_deaths="<b>{0}</b>".format(china_deaths)
    
    china_deathsp=f'{int(df_recap["Deaths (+)"][df_recap["Country/Region"]=="China"]):,}'
    china_deathsp="<b>(+{0})</b>".format(china_deathsp)
    
    #Spain
    spain_deaths=f'{int(df_recap["Deaths"][df_recap["Country/Region"]=="Spain"]):,}'
    spain_deaths="<b>{0}</b>".format(spain_deaths)
    
    spain_deathsp=f'{int(df_recap["Deaths (+)"][df_recap["Country/Region"]=="Spain"]):,}'
    spain_deathsp="<b>(+{0})</b>".format(spain_deathsp)
    
    #Iran
    iran_deaths=f'{int(df_recap["Deaths"][df_recap["Country/Region"]=="Iran"]):,}'
    iran_deaths="<b>{0}</b>".format(iran_deaths)
    
    iran_deathsp=f'{int(df_recap["Deaths (+)"][df_recap["Country/Region"]=="Iran"]):,}'
    iran_deathsp="<b>(+{0})</b>".format(iran_deathsp)
    
    values_H4=[[china_deaths,china_deathsp],[france_deaths,france_deathsp],\
               [germany_deaths,germany_deathsp],[us_deaths,us_deathsp],\
               [spain_deaths,spain_deathsp], [iran_deaths,iran_deathsp],\
               [italy_deaths,italy_deathsp]]
    
    fig_H4= go.Figure(data=[go.Table(
      header=dict(values=["China","France", "Germany"\
                          ,"US","Spain","Iran"\
                          ,"Italy"]
        ,
        line_color=line_color_H2,fill_color=fill_color_H2,
        align='center',font=dict(color='black', size=10)
      ),
      cells=dict(
              line_color=line_color_H2,fill_color=fill_color_H2,font_color=font_color_H2,
        values=values_H4, font_size=13
        ))
    ])
    
    fig_H4.update_layout(
        autosize=False,
        width=1000,
        height=170,
        margin=dict(
            l=300,
            r=20,
            b=0,
            t=40,
            pad=20
        ),
        title_text="<b>DEATHS</b>",title_x=0.63,
       title_font_color='black'
    )                 
    return fig_H4


@app.callback(
    dash.dependencies.Output('outputfigure4', 'figure'),
   [dash.dependencies.Input('inputdate', 'value'), 
    dash.dependencies.Input('inputprevious', 'value')])
def updatefigure3(valued,valuep):
    previous=int(valuep)
    date=valued
    df_recap=GetData.get_recap_by_country(date,previous=previous)
    
    fill_color_H2='lightgray'
    line_color_H2='lightgray'
    font_color_H2=[['black','red']]
    font_size_H2=[12,11,11,11,11,11,11]
    
    columns_=["Country", "New Cases", "Total Cases","New Deaths","Total Deaths","Fatality", "Recovered"]
    columns_=['<b>{0}</b>'.format(i) for i in columns_]
    df_H5=pd.DataFrame(columns=["Country", "New Cases", "Total Cases","New Deaths","Total Deaths","Fatality", "Recovered"])

    
    df_H5["Country"]=x = ['<b>{0}</b>'.format(i) for i in df_recap["Country/Region"]]
    
    df_H5["Total Cases"]=df_recap["Cases"]
    
    df_H5["Total Deaths"]=df_recap["Deaths"]
    
    df_H5["Fatality"]=df_H5["Total Deaths"]/df_H5["Total Cases"]
    
    df_H5["Total Deaths"]=df_recap["Deaths"]
    
    df_H5["Recovered"]=df_recap["Recovered"]
    
    df_H5["New Cases"]=[f'{i:,}'for i in df_recap["Cases (+)"]]
    
    df_H5["New Cases"]=["(+{0})".format(str(i)) for i in df_H5["New Cases"]]
    
    df_H5["New Deaths"]=[f'{i:,}'for i in df_recap['Deaths (+)']]
    
    df_H5["New Deaths"]=["(+{0})".format(str(i)) for i in df_H5["New Deaths"]]
    
    df_H5["Fatality"]=["{:.2%}".format(i) for i in df_H5["Fatality"]]
    
    df_H5["Recovered"]=[f'{i:,}'for i in df_H5["Recovered"]]
    
    df_H5["Total Cases"]=[f'{i:,}'for i in df_H5["Total Cases"]]
    
    df_H5["Total Deaths"]=[f'{i:,}'for i in df_H5["Total Deaths"]]
    
    font_color_H5=['black','red','black','red','black','red','black']
    
    fig_H5 = go.Figure(go.Table(
        header=dict(values=list(columns_),
                    
                    align ='center', font=dict(color='black',size=12),
                    line_color=line_color_H2,
                    fill_color=fill_color_H2), 
                                
        cells=dict(values=[df_H5.Country, df_H5["New Cases"],df_H5["Total Cases"]\
                           , df_H5["New Deaths"], df_H5["Total Deaths"],\
                           df_H5.Fatality, df_H5.Recovered],
                   
                   font_size=font_size_H2,font_color=font_color_H5,
                   line_color=line_color_H2,fill_color=fill_color_H2)))
    
    
    fig_H5.update_layout(
        autosize=False,
        width=1000,
        height=400,
        margin=dict(
            l=300,
            r=20,
            b=100,
            t=50,
            pad=400
        ),
        title_text="<b>BY COUNTRY</b>",title_x=0.63,
       title_font_color='black'
    ) 
    return fig_H5
    