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
url = "https://github.com/10Dennisw/economics-africa-dashboard/raw/master/africa_economics_v2.csv"
df = pd.read_csv(url)
filtered_df_map=df[df['Year']==2000]

############################################################################################################
# Defining layout for Page 3 with a bar chart
layout = html.Div(style={'backgroundColor': 'white', 'color': '#FFFFFF', 'margin': '0', 'width': '1000px'}, children=[
    html.Div(style={'backgroundColor': 'white', 'width': '990px', 'border': '2px solid black', 'margin-left': '5px', 'margin-right': '5px'}, children=[
        html.B('Select Year to Filter On:', className = 'fix_label', style = {'color': 'black', 'paddingLeft': '20px'}),
        dcc.Slider(
            id='year-slider-page-three',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=df['Year'].min(), # setting the default value
            marks={
                str(year): {'label': str(year), 'style': {'color': 'black'}}  # Setting label color to black
                for year in range(df['Year'].min(), df['Year'].max() + 1)
                },
            step=1
        ),
    ]),
    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[
        dcc.Graph(
            id='gdp-per-capita-graph',
            style={'border': '2px solid black', 
                   'height': '375px', 'width': '100%', 
                   'margin-left': '5px', 'margin-right': '5px', 'margin-top': '6px', 'margin-bottom': '1px', 
                   'backgroundColor': '#000000'},
                )
    ]),

    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[   
        # Setting the format for the line chart
        dcc.Graph(id='histogram-chart',
                  style={'border': '2px solid black', 
                         'height': '375px', 'width': '49%', 
                         'float': 'left',
                         'margin-left': '5px', 'margin-right': '10px','margin-top': '5px', 'margin-bottom': '1px', 
                         'backgroundColor': '#000000'}       
        ),
        # Setting the format for the bar chart
        dcc.Graph(id='bar-chart',
            style={'border': '2px solid black', 
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

    map_fig = go.Figure(go.Choropleth(
        locations=filtered_df_map['Code'],  # Assuming 'Code' is the column with country codes
        z=np.log(filtered_df_map['GDP per Capita']),  # Logarithm of GDP per Capita
        hoverinfo='location+text',
        text=filtered_df_map['Country'],  # Country names for hover text
        hovertemplate='%{text}<br>GDP per Capita: %{z:.2f}',  # Custom hover template
        colorscale='Reds',
        colorbar_title='GDP (log)',
        marker_line_color='white',  # Line color between countries
        marker_line_width=0.5
    ))

    # Update the layout
    map_fig.update_layout(
        title=dict(
            text=f'<b>Map of the Logarithm of GDP per Capita in {selected_year}</b>',
            x=0.5  # Center the title
            ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            showcountries=True,
            countrycolor="#d1d1d1",
            showocean=True,
            oceancolor="#c9d2e0",
            showlakes=True,
            lakecolor="#99c0db",
            showrivers=True,
            rivercolor="#99c0db",
            projection_type='orthographic'
            ),
        paper_bgcolor="white",
        font=dict(color="black"),
        margin=dict(l=20, r=20, t=40, b=10)
    )
    
    # setting the border line width
    map_fig.update_traces(marker=dict(line={"color": "black", "width": 1.5}))
    
    # setting the map to focus on Africa
    map_fig.update_geos(projection_rotation=dict(lon=17, lat=2)) 
    map_fig.update_geos(projection_scale=1.43)  # updating zoom 

    map_fig.add_trace(go.Scattergeo(
        lon=[55.4920],  # Longitude for Seychelles 
        lat=[-4.6796],  # Latitude for Seychelles
        mode='markers',
        marker=dict(
            size=10,
            color='rgba(255, 0, 0, 0)',
            line=dict(width=1, color='black')
        ),
        name='Seychelles',
        showlegend=False
    ))

    map_fig.add_trace(go.Scattergeo(
        lon=[57.5522],  # Longitude for Mauritius
        lat=[-20.3484],  # Latitude for Mauritius
        mode='markers',
        marker=dict(
            size=10,
            color='rgba(255, 0, 0, 0)', 
            line=dict(width=1, color='black')
        ),
        name='Mauritius',
        showlegend=False
    ))

    map_fig.add_annotation(
        text="<b>Equitorial Guinea</b>",
        x=0.46, 
        y=0.5,  
        showarrow=True,
        arrowhead=1,
        arrowcolor="black",
        arrowwidth=2,
        ax=-200,
        ay=0,
        font=dict(size=12),
        bgcolor="white",  
        bordercolor="black",  
        borderwidth=1  
    )

    map_fig.update_layout(
        margin=dict(r=100)  # Increase the right margins for images
    )    

    map_fig.update_layout(
        annotations=[
            dict(
                text="<b>Equitorial Guinea</b>",
                x=0.46,  
                y=0.52, 
                showarrow=True,
                arrowhead=1,
                arrowcolor="black",
                arrowwidth=2,
                ax=-200,
                ay=0,
                font=dict(size=12),
                bgcolor="white",  
                bordercolor="black",  
                borderwidth=1  
            ),
            dict(
                x=0.67,
                y=0.43,
                xref="paper",
                yref="paper",
                showarrow=True,
                arrowhead=0,
                arrowcolor="black",
                arrowwidth=2,
                ax=157,
                ay=-170,
            ),
            dict(
                x=0.67,
                y=0.405,
                xref="paper",
                yref="paper",
                showarrow=True,
                arrowhead=0,
                arrowcolor="black",
                arrowwidth=2,
                ax=157,
                ay=-67,
            ),
            dict(
                x=0.67,
                y=0.24,
                xref="paper",
                yref="paper",
                showarrow=True,
                arrowhead=0,
                arrowcolor="black",
                arrowwidth=2,
                ax=113.5,
                ay=-20,
            ),
            dict(
                x=0.67,
                y=0.22,
                xref="paper",
                yref="paper",
                showarrow=True,
                arrowhead=0,
                arrowcolor="black",
                arrowwidth=2,
                ax=113,
                ay=36,
            ),
            dict(
                text="<b>Seychelles</b>",
                xref="paper", 
                yref="paper",
                x=0.9,  
                y=0.96,  
                showarrow=False, 
                font=dict(size=12),  
                align="center",  
                xanchor="center", 
                yanchor="bottom" ,
                bgcolor="white",  
            ),
            dict(
                text="<b>Mauritius</b>",
                xref="paper", 
                yref="paper",
                x=0.84,  
                y=0.32,  
                showarrow=False, 
                font=dict(size=12),  
                align="center",  
                xanchor="center", 
                yanchor="bottom" ,
                bgcolor="white", 
            ),
        ]),

    x0_seychelles, y0_seychelles = 0.85, 0.6
    sizex_seychelles = 0.15
    sizey_seychelles = 0.35

    map_fig.add_shape(type="rect",
        x0=x0_seychelles, y0=y0_seychelles, x1=x0_seychelles+sizex_seychelles, y1=y0_seychelles+sizey_seychelles,
        line=dict(color="red", width=1),
        fillcolor="white",
        xref="paper", yref="paper",
        layer="below"
    )

    map_fig.add_layout_image(dict(
        source="https://raw.githubusercontent.com/10Dennisw/economics-africa-dashboard/master/Seychellen-512.webp",
        x=x0_seychelles, y=y0_seychelles-0.02,
        xref="paper", yref="paper",
        sizex=0.4, sizey=0.4,
        xanchor="left", yanchor="bottom",
        layer="above"
    ))

    x0_mauritius, y0_mauritius= 0.8, 0.11
    sizex_mauritius = 0.07
    sizey_mauritius = 0.20

    map_fig.add_shape(type="rect",
        x0=x0_mauritius, y0=y0_mauritius, x1=x0_mauritius+sizex_mauritius, y1=y0_mauritius+sizey_mauritius,
        line=dict(color="red", width=1),
        fillcolor="white",
        xref="paper", yref="paper",
        layer="below"
    )

    map_fig.add_layout_image(dict(
        source="https://raw.githubusercontent.com/10Dennisw/economics-africa-dashboard/master/mauritius_img.png",
        x=x0_mauritius, y=y0_mauritius,
        xref="paper", yref="paper",
        sizex=0.2, sizey=0.2,
        xanchor="left", yanchor="bottom",
        layer="above"
    ))



   # map_fig.update_layout_images(dict(
    #        xref="paper",
    #        yref="paper",
    #        sizex=0.3,
     #       sizey=0.3,
     #       xanchor="right",
      #      yanchor="bottom"
    #))
    ############################################################################################################
    # Creating Histogram figure
    hist_fig = px.histogram(filtered_df, 
                            x='GDP per Capita', 
                            nbins=50, 
                            title=f'<b>Top 10 Economies (GDP per Capita) in {selected_year}</b>', 
                            labels={'GDP per Capita': 'GDP per Capita', 'count': 'Frequency'})
    
    # adding a black outline around the each bar of the histogram
    hist_fig.update_traces(marker_line_color='black', marker_line_width=1.5)

    hist_fig.update_layout(title_x=0.5, # setting the title to be in the middle of the figure
                           font=dict(color="black")
                           )

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
        y0=-0.4,
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
        font=dict(color="black")
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