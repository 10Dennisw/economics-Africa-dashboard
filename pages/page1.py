# importing libraries
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import copy
from plotly.subplots import make_subplots
import numpy as np

# defining name of page and path
dash.register_page(__name__, path='/', name="Evolution of African GDP: Overview")

# loading the data
url = "https://github.com/10Dennisw/economics-africa-dashboard/raw/master/africa_economics_v2.csv"
df = pd.read_csv(url)

# defining the layout of the page
layout = html.Div(style={'backgroundColor': 'white', 'color': '#FFFFFF', 'margin': '0', 'width': '1000px'}, children=[
    html.Div(style={'backgroundColor': 'white', 'width': '990px', 'border': '2px solid black', 'margin-left': '5px', 'margin-right': '5px'}, children=[
        html.B('Select Year to Filter On:', className = 'fix_label', style = {'color': 'black', 'paddingLeft': '20px'}),
        # creating a slider for each year, allowing the user to select a year to filter on
        dcc.Slider(
            id='year-slider',
            min=df['Year'].min(),  
            max=df['Year'].max(),  
            value=df['Year'].min(), # setting the default value
            marks={
                str(year): {'label': str(year), 'style': {'color': 'black'}}  # Setting label color to black
                for year in range(df['Year'].min(), df['Year'].max() + 1)
                },
            step=1, # setting each step as one year
        ), 
    ]),
    # Creating a 2 maps to be side by side - using 49% width.
    # The first map is just a chloropleth map, while the second map has an additional layer above, showing the population
    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[
        # Setting the format for the first map
        dcc.Graph(
            id='world-map',
            # defining the style of figure
            style={'border': '2px solid black', 
                   'height': '375px', 'width': '490px', 
                   'float': 'left',
                   'margin-left': '5px', 'margin-right': '10px','margin-top': '10px', 'margin-bottom': '5px', 
                   'backgroundColor': '#000000'}
        ),
        
        # Setting the format for the second map
        dcc.Graph(
            id='world-map-with-population',
            # defining the style of figure
            style={'border': '2px solid black', 
                   'height': '375px', 'width': '490px', 
                   'float': 'right', 'margin-top': '10px', 'margin-right': '5px', 'margin-bottom': '5px', 
                   'backgroundColor': '#000000'}
        ),
    ]),
    
    # Having an additional row, which also has two different charts. A bar chart and pie chart
    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[   
        # Setting the format for the bar chart
        dcc.Graph(
            id='gdp-bar-chart',
            style={'border': '2px solid black', 
                   'height': '375px', 'width': '490px', 
                   'float': 'left',
                   'margin-left': '5px', 'margin-right': '10px','margin-top': '5px', 'margin-bottom': '1px', 
                   'backgroundColor': '#000000'}       
        ),

        # Setting the format for the pie chart
        dcc.Graph(
            id='gdp-pie-chart',
            style={'border': '2px solid black', 
                   'height': '375px', 'width': '490px', 
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
    [Input('year-slider', 'value')],
    allow_duplicate=True
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

    ############################################################################################################
    # MAP CHARTS
    
    # defining the features of the choropleth Map
    map_fig = px.choropleth(
        filtered_df,
        locations='Code',
        color=np.log(filtered_df['GDP (USD)']),
        hover_name='Country',
        hover_data={'Code': False, 'GDP (USD)': ':,'},
        custom_data=[filtered_df['GDP (USD)']],
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
        hover_data={'Code': False, 'GDP (USD)': ':,', 'Population': ':,'},
        projection='orthographic',
        title='',
        template='plotly',
        opacity=0.5
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
    map_fig.update_geos(projection_rotation=dict(lon=17, lat=2)) # setting the map to focus on Africa
    map_fig.update_geos(projection_scale=1.43)  # updating zoom

    map_fig2= copy.deepcopy(map_fig) # creating a deepcopy of the map to avoid changes being updated to both maps
    
    map_fig.update_layout(title_text="<b>Chloropleth Map of GDP (log)</b>",
                          title_x=0.5)
    
    map_fig.add_annotation(
        text="<b>As the year increases,<br>watch the shade of red<br>increase as Africa's<br>economies grow larger</b>",
        xref="paper", 
        yref="paper",
        x=0.18,  
        y=0.25,  
        showarrow=False, 
        font=dict(size=12),  
        align="center",  
        xanchor="center", 
        yanchor="bottom" ,
        bgcolor="white",  
        bordercolor="black",  
        borderwidth=1   
    )

    map_fig_with_population = map_fig2.add_trace(scattergeo_fig.data[0]) # adding the population bubbles to the chloropleth map
    map_fig_with_population.update_layout(title_text="<b>Map of GDP (log) with Population Bubbles</b>",
                                          title_x=0.5)
    
    map_fig_with_population.add_annotation(
        text="<b>Nigeria is Africa's<br>most populous<br>economy</b>",
        x=0.36,  # Adjusted longitude for Nigeria
        y=0.54,  # Adjusted latitude for Nigeria
        showarrow=True,
        arrowhead=1,
        arrowcolor="black",
        arrowwidth=2,
        ax=-55,
        ay=100,
        font=dict(size=12),
        bgcolor="white",  
        bordercolor="black",  
        borderwidth=1  
    )

    ############################################################################################################
    # BAR CHART
    
    # creating as new df to get top five values of GDP
    top_five_df = filtered_df.sort_values(by='GDP (USD)', ascending=False).head(5)

    # defining the features of the bar chart Map
    bar_fig = px.bar(
        top_five_df,
        x='Country',
        y='GDP (USD)',
        title=f'<b>Largest 5 African Economies in {selected_year}</b>',
        labels={'GDP (USD)': 'GDP (USD in Billions)'},
        hover_data={'GDP (USD)': ':,', 'Population': ':,'},
        color='Country', # introducing colour to have different colour based upon country
        color_discrete_map=country_colours # setting it to country colour dictionairy
    )

    # rotating the angle of the x-axis labels to 25 degrees
    bar_fig.update_layout(xaxis_tickangle=25)
    # Addinga black outline of each bar
    bar_fig.update_traces(marker_line_color='black', marker_line_width=2)
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

    bar_fig.add_annotation(
        text="<b>As the year increases,<br>watch the bars of<br>Africa's largest five<br>economies grow taller</b>",
        xref="paper", 
        yref="paper",
        x=0.7,  
        y=0.8 ,  
        showarrow=False, 
        font=dict(size=12),  
        align="center",  
        xanchor="center", 
        yanchor="bottom" ,
        bgcolor="white",  
        bordercolor="black",  
        borderwidth=1   
    )

    
    ############################################################################################################
    # PIE CHART

    # function for getting the labels and values for the pie chart
    def getting_labels_and_values(filtered_df):
        ''' 
        Function to retrieve the largest economies in the df and retrieve the values, 
        setting other economies not in the Top 5 to other
        Input arguments: dataframe
        Returns list of labels and values
        '''
        pie_df = filtered_df.sort_values(by='GDP (USD)', ascending=False) # sorting values
        top5_indices = pie_df['GDP (USD)'].nlargest(5).index # getting index for top 5 largest
        pie_df.loc[~pie_df.index.isin(top5_indices), 'Country'] = 'Other' #setting countries not in top5_indices to 'Other'

        pie_df = pie_df.groupby('Country').sum().reset_index() # grouping the df by country/ economy

        # creating empty lists
        label_lst = []
        values_lst = []

        # iterating through df and appending label and value to list
        for i, r in pie_df.iterrows():
            country = r['Country']
            GDP = r['GDP (USD)']
            label_lst.append(country)
            values_lst.append(GDP)

        return label_lst, values_lst

    # Sorting and filtering the filtered dataframe to show 6 values, largest 5 economies and the other economies combined 
    pie_df = filtered_df.sort_values(by='GDP (USD)', ascending=False)
    top5_indices = pie_df['GDP (USD)'].nlargest(5).index
    pie_df.loc[~pie_df.index.isin(top5_indices), 'Country'] = 'Other' #setting countries not in top5_indices to 'Other'

    grouped_df = pie_df.groupby('Country').agg({
        'GDP (USD)': 'sum',
        'Population': 'sum'
    }).reset_index()
    grouped_df

    label_lst, valueslst = getting_labels_and_values(pie_df)

    text_lst = []
    for value in valueslst:
        text_lst.append(round(value/10**10,2))

    population_lst = []
    for i, r in grouped_df.iterrows():
        population_lst.append(r['Population'])


    # Features of the pie chart
    pie_fig = go.Figure(go.Pie(
        name = "",
        values = valueslst,
        labels = label_lst,
        text = text_lst,
        marker=dict(colors=[country_colours[label] for label in label_lst]),
        hovertemplate = "%{label}: %{text} Billion USD<br>Population: %{customdata:,}",
        textinfo='percent',
        customdata=population_lst
    ))

    # Setting the layout for the pie chart
    pie_fig.update_layout(
        paper_bgcolor="white",
        font=dict(color="black"),
        title=dict(x=0.5),
        margin=dict(l=30, r=30, t=60, b=60),
    )

    pie_fig.update_layout(title_text=f'<b>African GDP Distribution in {selected_year}</b>',
                          title=dict(x=0.5),
                          font=dict(color="black")
                          )

    # Adding a black outline around each section of the piece, and setting the width to black
    pie_fig.update_traces(marker=dict(line=dict(color='black', width=2)),
                        insidetextfont=dict(color='black', family="Arial", size=12)) 
    
    if selected_year == 2000:
        SA_pop = filtered_df[filtered_df['Country'] == 'South Africa']['Population'].iloc[0]
        total_population = filtered_df['Population'].sum()

        SA_gdp = filtered_df[filtered_df['Country'] == 'South Africa']['GDP (USD)'].iloc[0]
        total_gdp = filtered_df['GDP (USD)'].sum()

        pie_fig.add_annotation(
            text=f"<b>Despite having {round((SA_pop/total_population)*100,2)}%<br>of Africa's recorded<br>population, it has<br>{round((SA_gdp/total_gdp)*100,2)}% of Africa's<br>total GDP</b>",
            xref="paper", 
            yref="paper",
            x=1.15,  
            y=0.05,  
            showarrow=False, 
            font=dict(size=12),  
            align="center",  
            xanchor="center", 
            yanchor="bottom" ,
            bgcolor="white",  
            bordercolor="black",  
            borderwidth=1   
        )

    # returning the map figure and bar chart
    return map_fig, map_fig_with_population, bar_fig, pie_fig