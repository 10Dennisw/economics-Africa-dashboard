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
app.layout = html.Div(style={'backgroundColor': '#000000', 'color': '#FFFFFF', 'margin': '0'}, children=[
    html.H1("African GDP Dashboard", style={'textAlign': 'center', 'color': '#FFFFFF', 'fontFamily': 'sans-serif',  'paddingTop': '30px'}),

    # Creating a slider for each year, allowing the user to filter
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max() + 1)},
        step=1,
    ),

    # Creating a chloropleth and bar chart, to be side by side - using 49% width
    html.Div(style={'display': 'flex', 'backgroundColor': '#000000'}, children=[
        # Chloropleth map
        dcc.Graph(
            id='world-map',
            style={'border': '1px solid purple', 'height': '400px', 'width': '49%', 'float': 'left', 'margin-left': '5px', 'margin-right': '10px', 'margin-top': '20px', 'margin-bottom': '20px', 'backgroundColor': '#000000'}
        ),

        # Bar chart
        dcc.Graph(
            id='gdp-bar-chart',
            style={'border': '1px solid purple', 'height': '400px', 'width': '49%', 'float': 'right', 'margin-right': '5px', 'margin-top': '20px', 'margin-bottom': '20px', 'backgroundColor': '#000000'}         
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

    # Filtering and Sorting data frame to get top five values
    top_five_df = filtered_df.sort_values(by='GDP (USD)', ascending=False).head(5)

    # Features of the bar chart Map
    bar_fig = px.bar(
        top_five_df,
        x='Country',
        y='GDP (USD)',
        text='GDP (USD)',
        title=f'Largest 5 African Economies in {selected_year}',
        labels={'GDP (USD)': 'GDP (USD in Billions)'}
    )

    map_fig.update_layout(
        paper_bgcolor = "#333333",
        font=dict(color="white")
    )

    bar_fig.update_layout(
        paper_bgcolor = "#333333",
        font=dict(color="white"),
        title=dict(x=0.5)
    )

    # returning the map figure and bar chart
    return map_fig, bar_fig

# running the app, as defined above
if __name__ == '__main__':
    app.run_server(debug=True)



