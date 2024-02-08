# importing libraries
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import copy
from plotly.subplots import make_subplots
import numpy as np

# defining name of page and path
dash.register_page(__name__, path='/', name="Evolution of African GDP: Overview")

# loading the data
url = "https://raw.githubusercontent.com/10Dennisw/visualisations/master/africa_economics_v2.csv"
df = pd.read_csv(url)

# defining the layout of the page
layout = html.Div(style={'backgroundColor': 'white', 'color': '#FFFFFF', 'margin': '0'}, children=[
    # creating a slider for each year, allowing the user to select a year to filter on
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),  
        max=df['Year'].max(),  
        value=df['Year'].min(), # setting the default value
        marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max() + 1)},
        step=1, # setting each step as one year
    ), 

    # Creating a 2 maps to be side by side - using 49% width.
    # The first map is just a chloropleth map, while the second map has an additional layer above, showing the population
    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[
        # Setting the format for the first map
        dcc.Graph(
            id='world-map',
            # defining the style of figure
            style={'border': '1px solid black', 
                   'height': '375px', 'width': '49%', 
                   'float': 'left',
                   'margin-left': '5px', 'margin-right': '10px','margin-top': '2px', 'margin-bottom': '5px', 
                   'backgroundColor': '#000000'}
        ),
        
        # Setting the format for the second map
        dcc.Graph(
            id='world-map-with-population',
            # defining the style of figure
            style={'border': '1px solid black', 
                   'height': '375px', 'width': '49%', 
                   'float': 'right', 'margin-top': '2px', 'margin-right': '5px', 'margin-bottom': '5px', 
                   'backgroundColor': '#000000'}
        ),
    ]),
    
    # Having an additional row, which also has two different charts. A bar chart and pie chart
    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[   
        # Setting the format for the bar chart
        dcc.Graph(
            id='gdp-bar-chart',
            style={'border': '1px solid black', 
                   'height': '375px', 'width': '49%', 
                   'float': 'left',
                   'margin-left': '5px', 'margin-right': '10px','margin-top': '5px', 'margin-bottom': '1px', 
                   'backgroundColor': '#000000'}       
        ),

        # Setting the format for the pie chart
        dcc.Graph(
            id='gdp-pie-chart',
            style={'border': '1px solid black', 
                   'height': '375px', 'width': '49%', 
                   'float': 'right', 
                   'margin-top': '5px', 'margin-right': '5px', 'margin-bottom': '1px', 
                   'backgroundColor': '#000000'}
        ),
    ]),
])

# callack used to create interactivity between the user (through the slider)
@callback(
    [Output('world-map', 'figure'),
     Output('world-map-with-population', 'figure'),
     Output('gdp-bar-chart', 'figure'),
     Output('gdp-pie-chart', 'figure')],
    [Input('year-slider', 'value')]
)

# function to update the charts based upon the year selected by the slider 
def update_charts(selected_year):

    # filter the df based upon the year selected by the user on the slider
    filtered_df = df.loc[df['Year'] == selected_year]

    # creating a dictionairy with countries and their respective colours
    country_colours = {
        'South Africa': 'rgb(255, 128, 0)', 
        'Egypt': 'rgb(213, 109, 225)',  
        'Nigeria': 'rgb(93, 247, 26)',  
        'Algeria': 'rgb(0, 255, 255)',  
        'Morocco': 'rgb(255, 178, 102)',  
        'Angola': 'rgb(255, 0, 0)',
        'Sudan': 'rgb(246, 29, 159)',
        'Other': 'rgb(255, 255, 0)'
        }

    # defining the features of the choropleth Map
    map_fig = px.choropleth(
        filtered_df,
        locations='Code',
        color=np.log(df['GDP (USD)']),
        hover_name='Country',
        color_continuous_scale='reds',
        projection='orthographic',
        title='',
        template='plotly',
        range_color=[min(np.log(df['GDP (USD)'])), max(np.log(df['GDP (USD)']))]
    )

    # defining the featured of the additional layer for the second map with population bubbles
    scattergeo_fig = px.scatter_geo(
        filtered_df,
        locations='Code',  
        size='Population',  
        hover_name='Country',
        projection='orthographic',
        title='',
        template='plotly',
        opacity=0.5
    )

    # creating as new df to get top five values of GDP
    top_five_df = filtered_df.sort_values(by='GDP (USD)', ascending=False).head(5)

    # defining the features of the bar chart Map
    bar_fig = px.bar(
        top_five_df,
        x='Country',
        y='GDP (USD)',
        title=f'<b>Largest 5 African Economies in {selected_year}</b>',
        labels={'GDP (USD)': 'GDP (USD in Billions)'},
        color='Country', # introducing colour to have different colour based upon country
        color_discrete_map=country_colours # setting it to country colour dictionairy
    )

    # rotating the angle of the x-axis labels to 25 degrees
    bar_fig.update_layout(xaxis_tickangle=25)
    # Addinga black outline of each bar
    bar_fig.update_traces(marker_line_color='black', marker_line_width=2)
    
    # Sorting and filtering the filtered dataframe to show 6 values, largest 5 economies and the other economies combined 
    pie_df = filtered_df.sort_values(by='GDP (USD)', ascending=False)
    top5_indices = pie_df['GDP (USD)'].nlargest(5).index
    pie_df.loc[~pie_df.index.isin(top5_indices), 'Country'] = 'Other' #setting countries not in top5_indices to 'Other'

    # Features of the pie chart
    pie_fig = px.pie(
        pie_df,
        names='Country',
        values='GDP (USD)',
        title=f'<b>African GDP Distribution in {selected_year}</b>',
        color='Country', # introducing colour to have different colour based upon country
        color_discrete_map=country_colours # setting it to country colour dictionairy
    )

    # customising the appearance and marker traces in both map figures
    map_fig.update_traces(marker=dict(line={"color": "black", "width": 1.5}))

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
        margin=dict(l=20, r=20, t=40, b=10)
    )
    
    # working on map figures
    map_fig.update_geos(projection_rotation=dict(lon=17, lat=0)) # setting the map to focus on Africa
    map_fig2= copy.deepcopy(map_fig) # creating a deepcopy of the map to avoid changes being updated to both maps
    map_fig.update_layout(title_text="<b>Chloropleth Map of GDP (log)</b>",
                          title_x=0.5)
    map_fig_with_population = map_fig2.add_trace(scattergeo_fig.data[0]) # adding the population bubbles to the chloropleth map
    map_fig_with_population.update_layout(title_text="<b>Map of GDP (log) with Population Bubbles</b>",
                                          title_x=0.5)

    # updating the layout for the bar charts
    bar_fig.update_layout(
        paper_bgcolor = "white",
        font=dict(color="black"),
        title=dict(x=0.5),
        margin=dict(l=30, r=30, t=60, b=60),
        # Editing the y-axis to be easier to interpret for the user
        yaxis=dict(tickvals = [100000000000, 200000000000, 300000000000, 400000000000, 500000000000, 600000000000],
                   ticktext = [100, 200, 300, 400, 500, 600],
                   range=[0, 600000000000]),
        legend_title_text='Country'
    )

    # Setting the layout for the pie chart
    pie_fig.update_layout(
        paper_bgcolor="white",
        font=dict(color="black"),
        title=dict(x=0.5),
        margin=dict(l=30, r=30, t=60, b=60),
        legend_title_text='Country' # setting the legend title
    )

    # Adding a black outline around each section of the piece, and setting the width to black
    pie_fig.update_traces(marker=dict(line=dict(color='black', width=2)),
                          insidetextfont=dict(color='black', family="Arial", size=16),
    )                   

    # returning the map figure and bar chart
    return map_fig, map_fig_with_population, bar_fig, pie_fig