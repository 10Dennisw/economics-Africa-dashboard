# Importing necessary libraries
import dash
from dash import dcc, html
from dash import Input, Output, callback
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# defining name of page and path
dash.register_page(__name__, path='/Page3', name="Africa: GDP per Capita")

############################################################################################################
# Loadung t=
url = "https://raw.githubusercontent.com/10Dennisw/visualisations/master/africa_economics_v2.csv"
df = pd.read_csv(url)
df= df.loc[df['Year']==2000]

############################################################################################################
# Creating a map figure

map_fig = px.choropleth(
    df,
    locations='Code',
    color= np.log(df['GDP per Capita']),
    hover_name='Country',
    color_continuous_scale='reds',
    projection='orthographic',
    title='',
    template='plotly',
    range_color=[min(np.log(df['GDP per Capita'])), max(np.log(df['GDP per Capita']))]
)

############################################################################################################
# Creating Histogram figure

hist_fig = px.histogram(df, x='GDP per Capita', nbins=50, title='GDP per Capita Distribution', labels={'GDP per Capita': 'GDP per Capita', 'count': 'Frequency'})

############################################################################################################
# Creating bar chart

# defining average value
average_val = df['GDP per Capita'].mean()
# filtering and sorting the dataframe to show the top 10 values in order
top_10 = df.nlargest(10, 'GDP per Capita')
top_10 = top_10.sort_values(by=['GDP per Capita'], ascending=True)

# creating a horizontal bar plot
bar_fig = go.Figure(go.Bar(
    y=top_10['Country'],
    x=top_10['GDP per Capita'],
    orientation='h'
))

# adding a vertical line to show average GDP per Capita
bar_fig.add_shape(
    type="line",
    x0=average_val,
    y0=0,
    x1=average_val,
    y1=len(top_10),
    line=dict(
        color="black",
        width=3,
        dash="dashdot"
        ),
    name='Average GDP per Capita'
    )

# adding titles and axis labels
bar_fig.update_layout(
    title='GDP per Capita',
    yaxis=dict(title='Country'),
    xaxis=dict(title='GDP per Capita')
)


############################################################################################################
# Defining layout for Page 3 with a bar chart
layout = html.Div([
    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[
        dcc.Graph(figure=map_fig,
                id='gdp-per-capita-graph',
                style={'border': '1px solid black', 'height': '375px', 'width': '100%', 'margin-left': '5px', 'margin-right': '5px', 'margin-top': '1px', 'margin-bottom': '1px', 'backgroundColor': '#000000'},
                )
    ]),

    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[   
        # Setting the format for the line chart
        dcc.Graph(figure=hist_fig,
            id='histogram-chart',
            style={'border': '1px solid black', 
                   'height': '375px', 'width': '49%', 
                   'float': 'left',
                   'margin-left': '5px', 'margin-right': '10px','margin-top': '5px', 'margin-bottom': '1px', 
                   'backgroundColor': '#000000'}       
        ),
        # Setting the format for the bar chart
        dcc.Graph(figure=bar_fig,
            id='bar-chart',
            style={'border': '1px solid black', 
                   'height': '375px', 'width': '49%', 
                   'float': 'right', 'margin-top': '5px', 'margin-right': '5px', 'margin-bottom': '1px', 
                   'backgroundColor': '#000000'}
        ),
    ]),
])
