# Importing necessary libraries
import dash
from dash import dcc, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# defining name of page and path
dash.register_page(__name__, path='/Page2', name="Africa's Top 5 Economies: Comparison between 2000 to 2022")

# loading the data
url = "https://raw.githubusercontent.com/10Dennisw/visualisations/master/africa_economics_v2.csv"
df = pd.read_csv(url)

# filtering the dataframe to 2000, and 2022
filtered_2000 = df[df['Year']==2000]
filtered_2022 = df[df['Year']==2022]

# dictionairy outlining country colours
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

# calling functions
label_2000_lst, values_2000_lst = getting_labels_and_values(filtered_2000)
label_2022_lst, values_2022_lst = getting_labels_and_values(filtered_2022)

# creating a subplot
pie_fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]])
# adding the figure on the left
pie_fig.add_trace(go.Pie(labels=label_2000_lst, 
                     values=values_2000_lst, 
                     scalegroup='one',
                     name="African GDP 2000",
                     marker=dict(colors=[country_colours[label] for label in label_2000_lst])), 
                     1, 1)
# adding the figure on the right
pie_fig.add_trace(go.Pie(labels=label_2022_lst, 
                     values=values_2022_lst, 
                     scalegroup='one',
                     name="African GDP 2022",
                     marker=dict(colors=[country_colours[label] for label in label_2022_lst])), 
                     1, 2)
# creating header for the subplot
pie_fig.update_layout(title_text="<b>Evolution of African GDP from 2000 to 2022</b>",
                      title=dict(x=0.5),
                      font=dict(color="black"))
# updating text on the subplot to make the figure easier to understand for the user
pie_fig.update_layout(annotations=[
    dict(
        text="<b>2000</b>",
        x=0.18,
        y=1.15,
        xref="paper",
        yref="paper",
        font=dict(size=12),
        showarrow=False
    ),
    dict(
        text="<b>2022</b>",
        x=0.81,
        y=1.15,
        xref="paper",
        yref="paper",
        font=dict(size=12),
        showarrow=False
    ),
    dict(
        text="<b>Pie size proportional to the total GDP in year</b>",
        showarrow=False,
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.15,
        font=dict(size=12)
    ),
])
# formating the traces to increase readability for the user
pie_fig.update_traces(marker=dict(line=dict(color='black', width=2)),
                      insidetextfont=dict(color='black', family="Arial", size=12))

############################################################################################################
# SCATTER PLOT

# defining the countries/ economies to look at 
country_lst = ['South Africa', 'Nigeria', 'Egypt', 'Algeria', 'Morocco']
# Using boolean indexing to filter rows
filtered_df = df[df['Country'].isin(country_lst)]
# initalisating scatter plot
scatter_fig = go.Figure()

# iterating over countries in list and creating a values for each country
for country in filtered_df['Country'].unique():
    country_data = filtered_df[filtered_df['Country'] == country]
    scatter_fig.add_trace(go.Scatter(
        x=country_data['Year'],
        y=country_data['GDP (USD)'],
        name=country,  # creating legend label
        line=dict(color=country_colours.get(country, 'rgb(0, 0, 0)'), width=3),  # default to black if country not found
    ))

# Updating layout of the scart
scatter_fig.update_layout(
    title='<b>GDP from 2000 to 2022</b>',
    title_x=0.5, # setting header in the middle
    font=dict(family="Arial", color='black'),
    xaxis_title='Year',
    yaxis_title='GDP (USD in Billions)',
    showlegend=True, 
    yaxis=dict(tickvals = [200000000000, 400000000000, 600000000000],
               ticktext = [200, 400, 600]),
)

############################################################################################################
# BAR CHART

# function to find the index of a word (country in this case) in a list
def finding_index (word, list):
    '''
    A function to find the index of the word input in the list input
    Input: word that the functions looks for
    Input: List that the function searches in
    Output: the index of the word
    '''
    other_index = None
    for i in range(len(list)):
        if list[i] == word:
            other_index = i
    return other_index

# finding an removing other in the list for 2000
other_index_2000 = finding_index('Other', label_2000_lst)
label_2000_lst.remove(label_2000_lst[other_index_2000])
values_2000_lst.remove(values_2000_lst[other_index_2000])

# finding an removing other in the list for 2022
other_index_2022 = finding_index('Other', label_2022_lst)
label_2022_lst.remove(label_2022_lst[other_index_2022])
values_2022_lst.remove(values_2022_lst[other_index_2022])

# creating a bar chart with two bars for each country, one for 2000 and one for 2022
bar_fig = go.Figure(data=[
    go.Bar(name='2000', x=label_2000_lst, y=values_2000_lst),
    go.Bar(name='2022', x=label_2022_lst, y=values_2022_lst)
])

# Changing the bar mode to group them together
bar_fig.update_layout(barmode='group',
                      title="<b>GDP Comparison: 2000 to 2022</b>",
                      font=dict(family="Arial", color='black'),
                      yaxis=dict(tickvals = [100000000000, 200000000000, 300000000000, 400000000000, 500000000000],
                                             ticktext = [100, 200, 300, 400, 500]),
)
# creating an outline around each bar
bar_fig.update_traces(marker_line_color='black', marker_line_width=2)

############################################################################################################
# Defining layout for Page 2 with a bar chart
layout = html.Div([
    html.Div(style={'backgroundColor': 'white', 'color': '#FFFFFF', 'margin': '0', 'width': '1000px'}, children=[
        dcc.Graph(figure=pie_fig,
                id='african-gdp-graph',
                style={'border': '1px solid black', 'height': '375px', 'width': '990px', 
                       'margin-left': '5px', 'margin-right': '5px', 'margin-top': '1px', 'margin-bottom': '1px', 
                       'backgroundColor': '#000000'},
                )
    ]),

    html.Div(style={'backgroundColor': 'white', 'color': '#FFFFFF', 'margin': '0', 'width': '1000px'}, children=[ 
        # Setting the format for the line chart
        dcc.Graph(figure=scatter_fig,
            id='scatter-chart',
            style={'border': '1px solid black', 
                   'height': '375px', 'width': '490px', 
                   'float': 'left',
                   'margin-left': '5px', 'margin-right': '10px','margin-top': '5px', 'margin-bottom': '1px', 
                   'backgroundColor': '#000000'}       
        ),
        # Setting the format for the bar chart
        dcc.Graph(figure=bar_fig,
            id='bar-chart',
            style={'border': '1px solid black', 
                   'height': '375px', 'width': '490px', 
                   'float': 'right', 'margin-top': '5px', 'margin-right': '5px', 'margin-bottom': '1px', 
                   'backgroundColor': '#000000'}
        ),
    ]),
])
