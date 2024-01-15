# Importing the libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import copy
from plotly.subplots import make_subplots
import numpy as np

# Loading data
df = pd.read_csv(r"C:\Users\denni\OneDrive\Desktop\african-economics-dashboard\africa_economics_v2.csv")

# Creating the app and the layout
app = dash.Dash(__name__)
app.layout = html.Div(style={'backgroundColor': 'white', 'color': '#FFFFFF', 'margin': '0'}, children=[
    html.H1("African GDP Dashboard", style={'textAlign': 'center', 'color': 'black', 'fontFamily': 'sans-serif',  'paddingTop': '10px'}), # creating the title of the dashboard

    # Creating a slider for each year, allowing the user to filter on the year
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),  # the minimum set as the minimum year in the dataframe
        max=df['Year'].max(),  
        value=df['Year'].min(),
        marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max() + 1)},
        step=1, # setting each step as one year
    ), 

    # Creating a 2 maps to be side by side - using 49% width.
    # The first map is just a chloropleth map, while the second map has an additional layer above, showing the population
    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[
        # Setting the format for the first map
        dcc.Graph(
            id='world-map',
            style={'border': '1px solid black', 'height': '400px', 'width': '49%', 'float': 'left','margin-left': '5px', 'margin-right': '10px','margin-top': '2px', 'margin-bottom': '5px', 'backgroundColor': '#000000'}
        ),
        
        # Setting the format for the second map
        dcc.Graph(
            id='world-map-with-population',
            style={'border': '1px solid black', 'height': '400px', 'width': '49%', 'float': 'right', 'margin-top': '2px', 'margin-right': '5px', 'margin-bottom': '5px', 'backgroundColor': '#000000'}
        ),
    ]),
    
    # This rows also has two different charts. A bar chart and pie chart. Both with 49% width
    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[   
        # Setting the format for the bar chart
        dcc.Graph(
            id='gdp-bar-chart',
            style={'border': '1px solid black', 'height': '400px', 'width': '49%', 'float': 'left','margin-left': '5px', 'margin-right': '10px','margin-top': '5px', 'margin-bottom': '1px', 'backgroundColor': '#000000'}       
        ),

        # Setting the format for the pie chart
        dcc.Graph(
            id='gdp-pie-chart',
            style={'border': '1px solid black', 'height': '400px', 'width': '49%', 'float': 'right', 'margin-top': '5px', 'margin-right': '5px', 'margin-bottom': '1px', 'backgroundColor': '#000000'}
        ),
    ]),
])

# Using callbacks to update choropleth map and bar chart based on selected year
@app.callback(
    [Output('world-map', 'figure'),
     Output('world-map-with-population', 'figure'),
     Output('gdp-bar-chart', 'figure'),
     Output('gdp-pie-chart', 'figure')],
    [Input('year-slider', 'value')]
)

# A function to update the charts based upon the year selected by the slider 
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

    # Defining the features of the choropleth Map
    map_fig = px.choropleth(
        filtered_df,
        locations='Code',
        color='GDP_log_column',
        hover_name='Country',
        color_continuous_scale='reds',
        projection='orthographic',
        title='',
        template='plotly',
        range_color=[min(df['GDP_log_column']), max(df['GDP_log_column'])]
    )

    # Defining the featured of the additional layer for the second map
    scattergeo_fig = px.scatter_geo(
        filtered_df,
        locations='Code',  
        size='Population ',  
        hover_name='Country',
        projection='orthographic',
        title='',
        template='plotly',
        opacity=0.5,
        # size_max=np.nanmax(df['Population '].values)
    )

    # Filtering and Sorting data frame to get top five values
    top_five_df = filtered_df.sort_values(by='GDP (USD)', ascending=False).head(5)

    # Defining the features of the bar chart Map
    bar_fig = px.bar(
        top_five_df,
        x='Country',
        y='GDP (USD)',
        title=f'<b>Largest 5 African Economies in {selected_year}</b>',
        labels={'GDP (USD)': 'GDP (USD in Billions)'},
        color='Country', # introducing colour to have different colour based upon country
        color_discrete_map=country_colours # setting it to country colour dictionairy
    )

    # Rotating the angle of the x-axis labels to 25 degrees
    bar_fig.update_layout(xaxis_tickangle=25)

    # Addinga black outline of each bar, setting the width to 2
    bar_fig.update_traces(marker_line_color='black', marker_line_width=2)
    
    # Sorting and filtering the filtered dataframe to show 6 values, largest 5 economies and the other economies 
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
    
    # setting the map to focus on Africa
    map_fig.update_geos(projection_rotation=dict(lon=17, lat=0))

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
        yaxis=dict(tickvals = [50000000000, 100000000000, 150000000000, 200000000000, 250000000000,
                               300000000000, 350000000000, 400000000000, 450000000000, 500000000000,
                               550000000000],
                   ticktext = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550],
                   range=[0, max(df['GDP (USD)'])]),
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

# running the app, as defined above
if __name__ == '__main__':
    app.run_server(debug=True)



