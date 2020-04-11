import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash
external_stylesheets = [dbc.themes.BOOTSTRAP,"https://use.fontawesome.com/releases/v5.8.1/css/all.css",'https://kit.fontawesome.com/3ee914798e.js']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                        dbc.CardBody(
                            [
                                html.Img(src='https://image.flaticon.com/icons/svg/2785/2785819.svg',width="70px",height="70px",style={'margin-top':'1em'}),
                                html.Div('125,000',style={
                                    'color':'rgb(255, 152, 1)',
                                    'font-weight':"bolder",
                                    'font-size':'27px'
                                }),
                                html.Div('Total cases')
                            ]
                        ),style={"height":"219px","margin-top":"1em","text-align":"center",'font-family':'Montserrat'},
                    ),
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Img(src='https://image.flaticon.com/icons/svg/2747/2747789.svg',width="70px",height="70px",style={'margin-top':'1em'}),
                        html.Div('125,000',style={
                            'color':'red',
                            'font-weight':"bolder",
                            'font-size':'27px'
                        }),
                        html.Div('Total deaths')
                    ]
                ),style={"height":"219px","margin-top":"1em","text-align":"center",'font-family':'Montserrat'},
            ),
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Img(src='https://image.flaticon.com/icons/svg/2750/2750656.svg',width="70px",height="70px",style={'margin-top':'1em'}),
                        html.Div('125,000',style={
                            'color':'#28a745',
                            'font-weight':"bolder",
                            'font-size':'27px'
                        }),
                        html.Div('Total recovered')
                    ]
                ),style={"height":"219px","margin-top":"1em","text-align":"center",'font-family':'Montserrat'},
            ),
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Img(src='https://image.flaticon.com/icons/svg/555/555418.svg',width="60px",height="54px"),
                        dbc.Row(
                            [
                                dbc.Table(
                                    [
                                        html.Thead(
                                            html.Tr(
                                                [
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2785/2785819.svg',width="32px",height="32px")
                                                    ),
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2747/2747789.svg',width="32px",height="32px")
                                                    ),
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2750/2750656.svg',width="32px",height="32px")
                                                    )
                                                ]
                                            )
                                        ),
                                        html.Tbody(
                                            [
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            '125 000',style={'color':'rgb(255, 152, 1)',
                                                                            'font-weight':"bolder"}
                                                        ),
                                                        html.Td(
                                                            '125 000',style={'color':'red',
                                                                            'font-weight':"bolder"}
                                                        ),
                                                        html.Td(
                                                            '125 000',style={'color':'#28a745',
                                                                            'font-weight':"bolder"}
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),style={"margin-top":"1em","text-align":"center",'font-family':'Montserrat'},
            ),
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Img(src='https://image.flaticon.com/icons/svg/321/321230.svg',width="60px",height="54px"),
                        dbc.Row(
                            [
                                dbc.Table(
                                    [
                                        html.Thead(
                                            html.Tr(
                                                [
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2785/2785819.svg',width="32px",height="32px")
                                                    ),
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2747/2747789.svg',width="32px",height="32px")
                                                    ),
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2750/2750656.svg',width="32px",height="32px")
                                                    )
                                                ]
                                            )
                                        ),
                                        html.Tbody(
                                            [
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            '125 000',style={'color':'rgb(255, 152, 1)',
                                                                            'font-weight':"bolder"}
                                                        ),
                                                        html.Td(
                                                            '125 000',style={'color':'red',
                                                                            'font-weight':"bolder"}
                                                        ),
                                                        html.Td(
                                                            '125 000',style={'color':'#28a745',
                                                                            'font-weight':"bolder"}
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),style={"margin-top":"1em","text-align":"center",'font-family':'Montserrat'},
            ),
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Img(src='https://image.flaticon.com/icons/svg/412/412828.svg',width="60px",height="54px"),
                        dbc.Row(
                            [
                                dbc.Table(
                                    [
                                        html.Thead(
                                            html.Tr(
                                                [
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2785/2785819.svg',width="32px",height="32px")
                                                    ),
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2747/2747789.svg',width="32px",height="32px")
                                                    ),
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2750/2750656.svg',width="32px",height="32px")
                                                    )
                                                ]
                                            )
                                        ),
                                        html.Tbody(
                                            [
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            '125 000',style={'color':'rgb(255, 152, 1)',
                                                                            'font-weight':"bolder"}
                                                        ),
                                                        html.Td(
                                                            '125 000',style={'color':'red',
                                                                            'font-weight':"bolder"}
                                                        ),
                                                        html.Td(
                                                            '125 000',style={'color':'#28a745',
                                                                            'font-weight':"bolder"}
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),style={"margin-top":"1em","text-align":"center",'font-family':'Montserrat'},
            )
        )
        
    ],style={
        'margin-right':'1em',
        'margin-left':'1em'
    }
    
)

if __name__ == '__main__':
    app.run_server(port =7777,debug=True)