import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import geopandas as gpd
import json
import base64

import sys
sys.path.append("/home/johan/flask/src/")

app = Dash(__name__)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Upload(
        id='slct_gjson',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_gjson', component_property='contents')]
)
def update_graph(option_slctd):

    container = "Loaded geojson file: {}".format(option_slctd)
    
    # remove 'data:application/geo+json;base64' from string
    _, content_data = option_slctd.split(',')

    # Decode the data into a string 
    content_data=base64.b64decode(content_data).decode('utf-8')

    #Convert to geojson format
    geopjson = json.loads(content_data)

    gdf = gpd.GeoDataFrame.from_features(geopjson)
    point = (gdf.centroid.x[0], gdf.centroid.y[0]) 

    # Plotly Express
    fig = px.scatter_mapbox(lat=[point[1]], lon=[point[0]]).update_layout(
        mapbox={
            "style": "open-street-map",
            "zoom": 16,
            "layers": [
                {
                    "source": json.loads(gdf.geometry.to_json()),
                    "below": "traces",
                    "type": "line",
                    "color": "purple",
                    "line": {"width": 1.5},
                }
            ],
        },
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        height=1000,
    )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)