# Importing necessary libraries
import dash
from dash import dcc, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px



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

fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                    subplot_titles=['Year 2000', 'Year 2022'])
fig.add_trace(go.Pie(labels=label_2000_lst, 
                     values=values_2000_lst, 
                     scalegroup='one',
                     name="African GDP 2000",
                     marker=dict(colors=[country_colours[label] for label in label_2000_lst])), 
                     1, 1)
fig.add_trace(go.Pie(labels=label_2022_lst, 
                     values=values_2022_lst, 
                     scalegroup='one',
                     name="African GDP 2022",
                     marker=dict(colors=[country_colours[label] for label in label_2000_lst])), 
                     1, 2)
fig.update_layout(title_text="<b>Evolution of African GDP from 2000 to 2022</b>",
                  title=dict(x=0.5),
                  font=dict(color="black")
                  )
fig.update_traces(marker=dict(line=dict(color='black', width=2)),
                  insidetextfont=dict(color='black', family="Arial", size=16))


# Defining layout for Page 2 with a bar chart
layout = html.Div([
   
    dcc.Graph(figure=fig,
              id='african-gdp-graph',
              style={'border': '1px solid black', 'height': '350px', 'margin-left': '1px', 'margin-right': '1px', 'margin-top': '1px', 'margin-bottom': '1px', 'backgroundColor': '#000000'},
              )
])

'''
figure=px.pie(names=label_2000_lst, 
                values=values_2000_lst, 
                title='Sample Bar Chart for Page 2',
                color=label_2000_lst, # introducing colour to have different colour based upon country
                color_discrete_map=country_colours), # setting it to country colour dictionairy),
style={'height': '400px'},
'''