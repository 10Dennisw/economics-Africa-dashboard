# Importing the libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# importing a stylesheet
external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

# creating app instance with multiple pages and stylesheet
app = dash.Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=external_css)

# defining the layout of  the web app
app.layout = html.Div([
	html.Br(),
	html.P('African GDP Multi Page Web App', className="text-dark text-center fw-bold fs-1", style={'width':'1000px'}),
    html.Div(children=[
	    dcc.Link(page['name'], href=page["relative_path"], className="btn btn-dark m-2 fs-5")\
			  for page in dash.page_registry.values()], 
			  style={'width': '1000px', 'margin': 'auto'} # setting width of the page links
	),
	dash.page_container
], style={'margin-left': '0', 'margin-right': '0', 'width': '1000px', 'padding': '0', 'margin': '0 auto'})

# running the code when the python script is ran
if __name__ == '__main__':
	app.run(debug=True)