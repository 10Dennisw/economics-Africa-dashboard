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
# Loading data
url = "https://raw.githubusercontent.com/10Dennisw/visualisations/master/africa_economics_v2.csv"
df = pd.read_csv(url)
filtered_df_map=df[df['Year']==2000]

############################################################################################################
# Defining layout for Page 3 with a bar chart
layout = html.Div(style={'backgroundColor': 'white', 'color': '#FFFFFF', 'margin': '0', 'width': '1000px'}, children=[
    dcc.Slider(
        id='year-slider-page-three',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(), # setting the default value
        marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max() + 1)},
        step=1
    ),

    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[
        dcc.Graph(
            id='gdp-per-capita-graph',
            style={'border': '1px solid black', 
                   'height': '375px', 'width': '100%', 
                   'margin-left': '5px', 'margin-right': '5px', 'margin-top': '1px', 'margin-bottom': '1px', 
                   'backgroundColor': '#000000'},
                )
    ]),

    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[   
        # Setting the format for the line chart
        dcc.Graph(id='histogram-chart',
                  style={'border': '1px solid black', 
                         'height': '375px', 'width': '49%', 
                         'float': 'left',
                         'margin-left': '5px', 'margin-right': '10px','margin-top': '5px', 'margin-bottom': '1px', 
                         'backgroundColor': '#000000'}       
        ),
        # Setting the format for the bar chart
        dcc.Graph(id='bar-chart',
            style={'border': '1px solid black', 
                   'height': '375px', 'width': '49%', 
                   'float': 'right', 'margin-top': '5px', 'margin-right': '5px', 'margin-bottom': '1px', 
                   'backgroundColor': '#000000'}
        ),
    ]),
])

# callack used to create interactivity between the user (through the slider)
@callback(
    [Output('gdp-per-capita-graph', 'figure'),
     Output('histogram-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('year-slider-page-three', 'value')],
    allow_duplicate=True
)

def update_charts(selected_year):
    # filter the df based upon the year selected by the user on the slider
    filtered_df = df.loc[df['Year'] == selected_year]

    ############################################################################################################
    # Creating Map Figure

    map_fig = px.choropleth(
    filtered_df_map,
    locations='Code',
    color= np.log(filtered_df['GDP per Capita']),
    hover_name='Country',
    color_continuous_scale='reds',
    projection='orthographic',
    title=f'<b>Map of the Logarithm of GDP per Capita in {selected_year}</b>',
    template='plotly',
    range_color=[min(np.log(filtered_df['GDP per Capita'])), max(np.log(filtered_df['GDP per Capita']))]
    )

    # Setting the layout of the map and customising the appearance
    map_fig.update_layout(geo=dict(showframe=False,
                                   showcoastlines=True,
                                    showcountries=True,
                                    countrycolor="#d1d1d1",
                                    showocean=True,
                                    oceancolor="#c9d2e0",
                                    showlakes=True,
                                    lakecolor="#99c0db",
                                    showrivers=True,
                                    rivercolor="#99c0db",
                                    resolution=110
                                    ),
        coloraxis_colorbar=dict(title="GDP (log)"), # the colour is denotated by the logarithm of the GDP
        paper_bgcolor = "white",
        font=dict(color="black"),
        margin=dict(l=20, r=20, t=40, b=10),
        title_x=0.5 # setting the title to be in the middle of the figure
        )
    
    # setting the border line width
    map_fig.update_traces(marker=dict(line={"color": "black", "width": 1.5}))
    
    # setting the map to focus on Africa
    map_fig.update_geos(projection_rotation=dict(lon=17, lat=0)) 

    ############################################################################################################
    # Creating Histogram figure
    hist_fig = px.histogram(filtered_df, 
                            x='GDP per Capita', 
                            nbins=50, 
                            title=f'<b>Top 10 Economies (GDP per Capita) in {selected_year}</b>', 
                            labels={'GDP per Capita': 'GDP per Capita', 'count': 'Frequency'})
    
    # adding a black outline around the each bar of the histogram
    hist_fig.update_traces(marker_line_color='black', marker_line_width=1.5)

    hist_fig.update_layout(title_x=0.5) # setting the title to be in the middle of the figure

    ############################################################################################################
    # Creating bar chart

    # defining average value through the median due to outliers
    average_val = filtered_df['GDP per Capita'].median()
    # filtering and sorting the dataframe to show the top 10 values in order
    top_10 = filtered_df.nlargest(10, 'GDP per Capita')
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
        title=f'<b>Top 10 Economies (GDP per Capita)</b>',
        title_x=0.5,
        yaxis=dict(title='Country'),
        xaxis=dict(title='GDP per Capita'),
    )

    # adding black outline around each bar
    bar_fig.update_traces(marker_line_color='black', marker_line_width=1.5)

    # adding annotation for medium line
    bar_fig.add_annotation(dict(font=dict(color='black',size=10),
                                x=0.1,
                                y=1.08,
                                showarrow=False,
                                text="<b>Medium GDP per Capita of African Economies</b>",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"
                                )
                            )

    return map_fig, hist_fig, bar_fig