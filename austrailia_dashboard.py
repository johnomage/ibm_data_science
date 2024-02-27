import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt

# Create app
app = dash.Dash(__name__)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the wildfire data into pandas dataframe
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

# Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()  # used for the names of the months
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Layout Section of Dash

# Task 2.1: Add the Title to the Dashboard
app.layout = html.Div(children=[
    html.H1('Australia Wildfire Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 26}),

    # Task 2.2: Add the radio items and a dropdown right below the first inner division
    # outer division starts
    html.Div([
        # First inner divsion for  adding dropdown helper text for Selected Drive wheels
        html.Div([
            html.H2("Select Region:"),

            # Radio items to select the region
            dcc.RadioItems(
                options=[
                    {"label": "New South Wales", "value": "NSW"},
                    {"label": "Victoria", "value": "VIC"},
                    {"label": "Queensland", "value": "QLD"},
                    {"label": "South Australia", "value": "SA"},
                    {"label": "Western Australia", "value": "WA"},
                    {"label": "Tasmania", "value": "TAS"},
                    {"label": "Northern Territory", "value": "NT"}
                ],
                value="NSW",
                id='region-selector',
                inline=True
            ),

            # Dropdown to select year
            html.Div([
                html.H2('Select Year:', style={'paddingRight': '30px'}), dcc.Dropdown(
                                                                                        id='year-selector',
                                                                                        options=[
                                                                                            {'label': str(year), 'value': year} for year in df['Year'].unique()
                                                                                        ],
                                                                                        value='2005',
                                                                                        clearable=False
                                                                                    )
            ]),
            # Second Inner division for adding 2 inner divisions for 2 output graphs
            # TASK 2.3: Add two empty divisions for output inside the next inner division.
            html.Div([

                html.Div([], id='pie-chart'),
                html.Div([], id='bar-chart')
            ], style={'display': 'flex'})

        ])
    ]),
    # outer division ends

])

# TASK 2.4: Add the Output and input components inside the app.callback decorator.
# Place to add @app.callback Decorator
@app.callback([Output(component_id='pie-chart', component_property='children'),
               Output(component_id='bar-chart', component_property='children')],
              [Input(component_id='region-selector', component_property='value'),
               Input(component_id='year-selector', component_property='value')])


# TASK 2.5: Add the callback function.
# Place to define the callback function .
def reg_year_display(input_region, input_year):

    # Data
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year'] == input_year]

    # Plot one - Monthly Average Estimated Fire Area
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    pie_fig = px.pie(est_data, values='Estimated_fire_area', names='Month',
                  title="{} : Monthly Average Estimated Fire Area in year {}".format(input_region, input_year))

    # Plot two - Monthly Average Count of Pixels for Presumed Vegetation Fires
    veg_data = y_r_data.groupby('Month')['Vegetation_index_mean'].mean().reset_index()
    bar_fig = px.bar(veg_data, x='Month', y='Vegetation_index_mean',
                  title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region, input_year))

    return [dcc.Graph(figure=pie_fig), dcc.Graph(figure=bar_fig)]


if __name__ == '__main__':
    app.run_server()
