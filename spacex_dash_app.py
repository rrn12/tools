# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
#read the csv file
max_payload = spacex_df['Payload Mass (kg)'].max()
#maximum payload
min_payload = spacex_df['Payload Mass (kg)'].min()
#minimum payload
e=dict()#diictionary class
for i in range(0,10500,500):#0 to 10000 with step 500
    e[i]=i
    #key=i, value=i
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),#title
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=[{'label':'All sites','value':'ALL'},
                                {'label':spacex_df['Launch Site'].unique()[0],
                                'value':spacex_df['Launch Site'].unique()[0]},
                                {'label':spacex_df['Launch Site'].unique()[1],
                                'value':spacex_df['Launch Site'].unique()[1]},
                                {'label':spacex_df['Launch Site'].unique()[2],
                                'value':spacex_df['Launch Site'].unique()[2]},
                                {'label':spacex_df['Launch Site'].unique()[3],
                                'value':spacex_df['Launch Site'].unique()[3]},],
                                #launch sites in dropdown
                                value='ALL',#default
                                placeholder='Select a Launch Site here',
                                searchable=True),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                #a chart area with id success-pie-chart
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks=e,
                                                value=[min_payload, max_payload]),
                                #slider with id payload-slider with 
                                #default position at maximum and minimum payload
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])#a chart area with id success-payload-scatter-chart

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart',
#output of callback is shown at chart area with id success-pie-chart
component_property='figure'),
              Input(component_id='site-dropdown',
              #input is dropdown option and 
              #the value of the option is argument in 
              #the decorator function
              component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':#if All sites selected
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='All Sites pie chart')
        return fig#pie chart for all sites
    else:
        filtered=filtered_df.loc[filtered_df['Launch Site']==entered_site]
        fig = px.pie(filtered, names='class',
        title=entered_site)
        return fig#pie chart of selected site
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', 
#output of callback is shown at chart area 
#with id success-payload-scatter-chart
component_property='figure'),
[Input(component_id='site-dropdown', 
component_property='value'), 
Input(component_id="payload-slider", 
component_property="value")])
#inputs are the dropdown option and payload slider range
def f(dropdown,slider):
    filtered=spacex_df.loc[(spacex_df['Payload Mass (kg)']>=min(slider))&(spacex_df['Payload Mass (kg)']<=max(slider))]
    #filter the data for data in slider range only
    if dropdown=='ALL':#if All sites selected
        figure=px.scatter(filtered,
        x='Payload Mass (kg)',
        y='class',
        color="Booster Version Category")
        return figure
        #scatterplot for all sites using 
        #colors for Booster Version Category
    else:
        filtered1=filtered.loc[filtered['Launch Site']==dropdown]
        #further filter the data for site in selected dropdown option only
        figure=px.scatter(filtered1,
        x='Payload Mass (kg)',
        y='class',
        color="Booster Version Category")
        return figure
        #scatterplot for selected site using 
        #colors for Booster Version Category
# Run the app
if __name__ == '__main__':
    app.run_server()
