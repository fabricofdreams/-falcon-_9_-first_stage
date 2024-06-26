# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Extract the unique launch sites and create dropdown options
launch_sites = spacex_df['Launch Site'].unique()
dropdown_options = [{'label': site, 'value': site} for site in launch_sites]
dropdown_options.insert(0, {'label': 'All Sites', 'value': 'ALL'})  # Add 'All Sites' option

# Min and max values to Select Payload
# Filter out the zero values
non_zero_payloads = spacex_df[spacex_df['Payload Mass (kg)'] > 0]
min_value = int(non_zero_payloads['Payload Mass (kg)'].min())
max_value = int(spacex_df['Payload Mass (kg)'].max())

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=dropdown_options,
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=500,
                                                marks={0: '0 Kg',
                                                    500: '500 Kg',
                                                    1000: '1000 Kg',
                                                    2000: '2000 kg',
                                                    5000: '5000 Kg',
                                                    7000: '7000 Kg',
                                                    10000: '10000 Kg'},
                                                value=[min_value, max_value]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df,
                     values='class',
                     names='Launch Site', 
                     title='Total Success Launches By All Sites',
                     hole=0.3)
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Total Success Launches for site {entered_site}',
                     hole=0.3)
    return fig      

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'), 
                Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site, entered_load):
    low, high = entered_load
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, 
                         x='Payload Mass (kg)', 
                         y='class',
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for All Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, 
                         x='Payload Mass (kg)', 
                         y='class',
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {entered_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
