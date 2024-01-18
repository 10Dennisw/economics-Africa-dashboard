# Importing necessary libraries
import dash
from dash import dcc, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



dash.register_page(__name__, path='/Page2', name="Page 2")

df = pd.read_csv(r"C:\Users\denni\OneDrive\Desktop\african-economics-dashboard\africa_economics_v2.csv")

filtered_2000 = df[df['Year']==2000]
filtered_2022 = df[df['Year']==2022]

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

def getting_labels_and_values(filtered_df):
    pie_df = filtered_df.sort_values(by='GDP (USD)', ascending=False)
    top5_indices = pie_df['GDP (USD)'].nlargest(5).index
    pie_df.loc[~pie_df.index.isin(top5_indices), 'Country'] = 'Other' #setting countries not in top5_indices to 'Other'

    pie_df = pie_df.groupby('Country').sum().reset_index()

    label_lst = []
    values_lst = []

    for i, r in pie_df.iterrows():
        country = r['Country']
        GDP = r['GDP (USD)']
        label_lst.append(country)
        values_lst.append(GDP)

    return label_lst, values_lst

label_2000_lst, values_2000_lst = getting_labels_and_values(filtered_2000)
label_2022_lst, values_2022_lst = getting_labels_and_values(filtered_2022)

pie_fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                    subplot_titles=['Year 2000', 'Year 2022'])
pie_fig.add_trace(go.Pie(labels=label_2000_lst, 
                     values=values_2000_lst, 
                     scalegroup='one',
                     name="African GDP 2000",
                     marker=dict(colors=[country_colours[label] for label in label_2000_lst])), 
                     1, 1)
pie_fig.add_trace(go.Pie(labels=label_2022_lst, 
                     values=values_2022_lst, 
                     scalegroup='one',
                     name="African GDP 2022",
                     marker=dict(colors=[country_colours[label] for label in label_2000_lst])), 
                     1, 2)
pie_fig.update_layout(title_text="<b>Evolution of African GDP from 2000 to 2022</b>",
                  title=dict(x=0.5),
                  font=dict(color="black")
                  )
pie_fig.update_traces(marker=dict(line=dict(color='black', width=2)),
                  insidetextfont=dict(color='black', family="Arial", size=16))


country_lst = ['South Africa', 'Nigeria', 'Egypt', 'Algeria', 'Morocco']
# Using boolean indexing to filter rows
filtered_df = df[df['Country'].isin(country_lst)]

scatter_fig = go.Figure()

# iterating over countries in list and creating a values for each country
for country in filtered_df['Country'].unique():
    country_data = filtered_df[filtered_df['Country'] == country]
    scatter_fig.add_trace(go.Scatter(
        x=country_data['Year'],
        y=country_data['GDP (USD)'],
        name=country  # creating legend label
    ))

# Updating layout of the scart
scatter_fig.update_layout(
    title='GDP over Time',
    xaxis_title='Year',
    yaxis_title='GDP (USD)',
    showlegend=True, 
)

# function to find the index of a word (country in this case) in a list
def finding_index (word, list):
    other_index = None
    for i in range(len(list)):
        if list[i] == word:
            other_index = i
    return other_index

# finding an removing other in the list 
other_index_2000 = finding_index('Other', label_2000_lst)
label_2000_lst.remove(label_2000_lst[other_index_2000])
values_2000_lst.remove(values_2000_lst[other_index_2000])

# finding an removing other in the list 
other_index_2022 = finding_index('Other', label_2022_lst)
label_2022_lst.remove(label_2022_lst[other_index_2022])
values_2022_lst.remove(values_2022_lst[other_index_2022])

bar_fig = go.Figure(data=[
    go.Bar(name='2000', x=label_2000_lst, y=values_2000_lst),
    go.Bar(name='2022', x=label_2022_lst, y=values_2022_lst)
])

# Changing the bar mode to group them together
bar_fig.update_layout(barmode='group')

# Defining layout for Page 2 with a bar chart
layout = html.Div([
    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[
        dcc.Graph(figure=pie_fig,
                id='african-gdp-graph',
                style={'border': '1px solid black', 'height': '375px', 'width': '100%', 'margin-left': '5px', 'margin-right': '5px', 'margin-top': '1px', 'margin-bottom': '1px', 'backgroundColor': '#000000'},
                )
    ]),

    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[   
        # Setting the format for the line chart
        dcc.Graph(figure=scatter_fig,
            id='scatter-chart',
            style={'border': '1px solid black', 'height': '375px', 'width': '49%', 'float': 'left','margin-left': '5px', 'margin-right': '10px','margin-top': '5px', 'margin-bottom': '1px', 'backgroundColor': '#000000'}       
        ),

        # Setting the format for the bar chart
        dcc.Graph(figure=bar_fig,
            id='bar-chart',
            style={'border': '1px solid black', 'height': '375px', 'width': '49%', 'float': 'right', 'margin-top': '5px', 'margin-right': '5px', 'margin-bottom': '1px', 'backgroundColor': '#000000'}
        ),
    ]),
])

'''
figure=px.pie(names=label_2000_lst, 
                values=values_2000_lst, 
                title='Sample Bar Chart for Page 2',
                color=label_2000_lst, # introducing colour to have different colour based upon country
                color_discrete_map=country_colours), # setting it to country colour dictionairy),
style={'height': '400px'},
'''