import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import os
import numpy as np

import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls

from sklearn.linear_model import LinearRegression

from shutil import copyfile


print("started")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
aircrafts_num = np.array(np.linspace(1, 30, 30, dtype=int))
available_models = ['linear']

df = pd.read_csv('../input/final_df_2020-12-03_16-45-50.csv')

asset_df = df[(df['aircraft_id'] == df['aircraft_id'].unique()[0])]
max_cicle = max(asset_df['cicle'].values)
asset_df['target'] = max_cicle - asset_df['cicle'].values
train_data = asset_df.copy()

for aircraft_id in df['aircraft_id'].unique()[1:]:
    asset_df = df[(df['aircraft_id'] == aircraft_id)]
    max_cicle = max(asset_df['cicle'].values)
    asset_df['target'] = max_cicle - asset_df['cicle'].values
    #print(asset_df.head())
    pd.concat([asset_df, train_data], sort=True)

#print('train_data', train_data.head())
X = train_data.drop(columns=['topic', 'measurement', 'aircraft_id', 'time', 'target']).values
Y = train_data['target'].values

linear_reg = LinearRegression().fit(X, Y)
print("lerned")


###############
app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in aircrafts_num],
                value='30'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_models],
                value='linear'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),
#################
    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            clickData={'points': [{'x': ' '}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'})
])
#########################

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type):

    # copyfile('../input/final_df_2020-12-03_16-45-50.csv', '../input/final_df_2020-12-03_16-45-50_copy.csv')
    df = pd.read_csv('../input/final_df_2020-12-03_16-45-50.csv')
    print("len df", len(df))

    fig = go.Figure()

    for aircraft_id in np.random.choice(df['aircraft_id'].unique(), int(xaxis_column_name)):
        # Add traces
        asset_df = df[(df['aircraft_id'] == aircraft_id)]

        fig.add_trace(go.Scatter(x=asset_df['time'].values,
                                 y=asset_df['cicle'].values,
                                 mode='lines+markers',
                                 name=str(aircraft_id)))

    return fig


def create_time_series(x, y, axis_type, title):

    fig = px.scatter(x=x, y=y, labels={'x':'time', 'y':'circle'})

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig

##############################
@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(clickData, xaxis_column_name, axis_type):

    aircraft_time = clickData['points'][0]['x']
    #print(aircraft_time)
    aircraft_time1 = aircraft_time[:10]+'T'+aircraft_time[11:]+'Z'
    #print(aircraft_time1)


    df = pd.read_csv('../input/final_df_2020-12-03_16-45-50.csv')
    #df.time = pd.to_datetime(df.time)

    #print(df['time'].values[0])

    index = df.index
    condition = df['time'].values == aircraft_time1
    apples_indices = index[condition]

    apples_indices_list = apples_indices.tolist()

    #print(apples_indices_list)
    if len(apples_indices_list) != 0:
        id = df.iloc[[apples_indices_list[0]]]['aircraft_id'].values[0]
        #print(id)
    else:
        id = df.aircraft_id.unique()[0]

    one_data = df[df.aircraft_id == id]
    title = 'aircraft id: <b>{}</b>'.format(id)
    return create_time_series(one_data["time"].values, one_data["cicle"].values, axis_type, title)

@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(clickData, yaxis_column_name, axis_type):

    aircraft_time = clickData['points'][0]['x']
    aircraft_time1 = aircraft_time[:10] + 'T' + aircraft_time[11:] + 'Z'

    df = pd.read_csv('../input/final_df_2020-12-03_16-45-50.csv')

    index = df.index
    condition = df['time'].values == aircraft_time1
    apples_indices = index[condition]

    apples_indices_list = apples_indices.tolist()

    # print(apples_indices_list)
    if len(apples_indices_list) != 0:
        id = df.iloc[[apples_indices_list[0]]]['aircraft_id'].values[0]
        #print(id)
    else:
        id = df.aircraft_id.unique()[0]

    one_data = df[df.aircraft_id == id]

    x = one_data['time'].values
    one_data = one_data.drop(columns=['topic', 'measurement', 'aircraft_id', 'time']).values
    y = linear_reg.predict(one_data)

    title = 'predictions by: <b>{}</b> model'.format(yaxis_column_name)
    return create_time_series(x, y, axis_type, title)


if __name__ == '__main__':
    app.run_server(debug=True)