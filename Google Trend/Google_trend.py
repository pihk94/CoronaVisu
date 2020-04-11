from pytrends.request import TrendReq
import plotly.graph_objects as go
from plotly.offline import plot
import pandas as pd

def google_trend_graph(w):

    pytrend = TrendReq()
    df = pd.DataFrame()
    for i in w:
        pytrend.build_payload(kw_list=[i], timeframe='today 3-m')
        interest_w = pytrend.interest_over_time() 
        df[i] = interest_w[i]

    fig_trend_w = go.Figure()
    for i in range(len(w)):
        fig_trend_w.add_trace(go.Scatter(x=df.index, y=df.iloc[:,i], mode='lines', name=w[i]))
    
    fig_trend_w.update_layout(
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
            plot_bgcolor='white')
    
    return fig_trend_w

word = ['carrefour', 'deliveroo', 'ubereats']
fig = google_trend_graph(word)
plot(fig, filename = 'Google Trend/google_trend_{}.html'.format(word))
