# Importing the libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Loading data
df = pd.read_csv(r"C:\Users\denni\OneDrive\Desktop\africa_economics_v2.csv")


# Creating the app and the layout
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("African GDP Dashboard"),
    
    # Creating a slider for each year, allowing the user to filter
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max() + 1)},
        step=1
    ),
    
    # Creating a chloropleth and bar chart, to be side by side - using 49% width
    html.Div([
        # Chloropleth map
        dcc.Graph(
            id='world-map',
            style={'border': '1px solid #ddd', 'height': '400px', 'width': '49%', 'float': 'left'}
        ),
        
        # Bar chart
        dcc.Graph(
            id='gdp-bar-chart',
            style={'border': '1px solid #ddd', 'height': '400px', 'width': '49%', 'float': 'right'}
        ),
    ]),
])

# Using callbacks to update choropleth map and bar chart based on selected year
@app.callback(
    [Output('world-map', 'figure'),
     Output('gdp-bar-chart', 'figure')],
    [Input('year-slider', 'value')]
)
def update_charts(selected_year):
    filtered_df = df.loc[df['Year'] == selected_year]
    
    # Features of the choropleth Map
    map_fig = px.choropleth(
        filtered_df,
        locations='Code',
        color='GDP (USD)',
        hover_name='Country',
        scope="africa",
        color_continuous_scale=px.colors.sequential.Plasma,
        projection='orthographic'
    )
    
    # Features of the bar chart Map
    bar_fig = px.bar(
        filtered_df,
        x='Country',
        y='GDP (USD)',
        text='GDP (USD)',
        title=f'GDP for {selected_year}',
        labels={'GDP (USD)': 'GDP (USD in Billions)'}
    )
    
    # returning the map figure and bar chart
    return map_fig, bar_fig

# running the app, as defined above
if __name__ == '__main__':
    app.run_server(debug=True)



