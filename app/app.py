import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from data import df_year_indicators
from callbacks import register_callbacks
import flask

# Dash app initiation

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Population Report'

# Dash app layout body

BODY = html.Div(className='wrapper ', children=[
    html.Div(className='sidebar', **{'data-color': 'white', 'data-active-color': 'danger'}, children=[
        html.Div(className='logo', children=[
            html.Img(className="simple-text logo-normal", src="./assets/icon/logo.png", style={'maxHeight': '80px', 'maxWidth': '60px', 'marginLeft': 'auto', 'marginRight': 'auto'})
        ]),
        html.Div(className="sidebar-wrapper", children=[
            html.Ul(className='nav', children=[
                html.Li(id="page-1-link", children=[
                    html.A(href='/population', children=[
                        html.I(className='nc-icon nc-single-02'),
                        html.P(['Population'])
                    ])
                ]),
                html.Li(id="page-2-link", children=[
                    html.A(href='/births', children=[
                        html.I(className='nc-icon nc-single-02'),
                        html.P(['Births'])
                    ])
                ]),
                html.Li(id="page-3-link", children=[
                    html.A(href='/deaths', children=[
                        html.I(className='nc-icon nc-single-02'),
                        html.P(['Deaths'])
                    ])
                ])
            ])
        ])
    ]),
    html.Div(className='main-panel', children=[
        dbc.Nav(className="navbar navbar-expand-lg navbar-absolute fixed-top navbar-transparent", children=[
            html.Div(className='container-fluid', children=[
                html.Div(className='navbar-wrapper', children=[
                    html.A(className='navbar-brand', href="#", style={'fontWeight': 'bold'}, children=['Population Report'])
                ]),
            ])
        ]),
        html.Div(className='content', children=[
            html.Div(className='row', children=[
                html.Div(className="col-md-1", children=[
                    html.Div(className="icon-big text-center icon-warning", children=[
                        html.Img(src="./assets/icon/visualize.png", style={'maxHeight': '80px', 'maxWidth': '60px', 'marginTop': -8})
                    ])
                ]),
                html.Div(className="col-md-11", children=[
                    html.H5(children=['Data Visualization'], style={'fontSize': 25, 'marginTop': 5}),
                ])
            ]),
            html.Div(className='row', children=[
                html.Div(className="col-md-12", children=[
                    html.Hr()
                ])
            ]),
            html.Div(className='row', children=[
                html.Div(className="col-md-12", children=[
                    html.Div(className='card ', children=[
                        html.Div(className='card-header ', children=[
                            html.H5(id='graph-title', className="card-title"),
                        ]),
                        html.Div(id='first-graph', className='card-body ', style={'marginTop': -30})
                    ])
                ])
            ]),
            html.Div(className='row', children=[
                html.Div(className="col-md-6", children=[
                    html.Div(className='card ', children=[
                        html.Div(className='card-header ', children=[
                            html.H5(className="card-title", children=['Year Selector']),
                        ]),
                        html.Div(id='content-slider', className='card-body ', style={'marginTop': -10, 'marginBottom': 5}, children=[
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id='year-dropdown',
                                        options = [{'label': i, 'value': i} for i in pd.to_datetime(df_year_indicators['DATE']).dt.year.unique()],
                                        value=2019,
                                        clearable=False
                                    ),
                                ],
                                md=12
                            ),
                        ])
                    ])
                ]),
                html.Div(className="col-md-6", children=[
                    html.Div(className='card ', children=[
                        html.Div(className='card-header ', children=[
                            html.H5(className="card-title", children=['Month Selector']),
                        ]),
                        html.Div(id='content', className='card-body ', style={'marginTop': -10, 'marginBottom': 5}, children=[
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id='month-dropdown',
                                        options=[
                                            {'label': 'January', 'value': 1},
                                            {'label': 'Febuary', 'value': 2},
                                            {'label': 'March', 'value': 3},
                                            {'label': 'April', 'value': 4},
                                            {'label': 'May', 'value': 5},
                                            {'label': 'June', 'value': 6},
                                            {'label': 'July', 'value': 7},
                                            {'label': 'August', 'value': 8},
                                            {'label': 'September', 'value': 9},
                                            {'label': 'October', 'value': 10},
                                            {'label': 'November', 'value': 11},
                                            {'label': 'December', 'value': 12}
                                        ],
                                        value=12,
                                        clearable=False
                                    ),
                                ],
                                md=12
                            )
                            
                        ])
                    ])
                ])
            ]),
            html.Div(className='row', children=[
                html.Div(id='first-content', children=[
                    html.Div(className="card card-stats", children=[
                        html.Div(className="card-body ", children=[
                            html.Div(className='row', children=[
                                html.Div(className="col-5 col-md-4", children=[
                                    html.Div(id='img-content-1', className="icon-big text-center icon-warning")
                                ]),
                                html.Div(className="col-7 col-md-8", children=[
                                    html.Div(className="numbers", children=[
                                        html.P(id='first-content-1', className="card-category"),
                                        html.P(id='first-content-2', className="card-title"),
                                    ])
                                ]),
                            ])
                        ]),
                    ])
                ]),
                html.Div(id='second-content', children=[
                    html.Div(className="card card-stats", children=[
                        html.Div(className="card-body ", children=[
                            html.Div(className='row', children=[
                                html.Div(className="col-5 col-md-4", children=[
                                    html.Div(id='img-content-2', className="icon-big text-center icon-warning")
                                ]),
                                html.Div(className="col-7 col-md-8", children=[
                                    html.Div(className="numbers", children=[
                                        html.P(id='second-content-1', className="card-category"),
                                        html.P(id='second-content-2', className="card-title"),
                                    ])
                                ]),
                            ])
                        ]),

                    ])
                ]),
                html.Div(id='third-content', children=[
                    html.Div(className="card card-stats", children=[
                        html.Div(className="card-body ", children=[
                            html.Div(className='row', children=[
                                html.Div(className="col-5 col-md-4", children=[
                                    html.Div(id='img-content-3', className="icon-big text-center icon-warning")
                                ]),
                                html.Div(className="col-7 col-md-8", children=[
                                    html.Div(className="numbers", children=[
                                        html.P(id='third-content-1', className="card-category"),
                                        html.P(id='third-content-2', className="card-title"),
                                    ])
                                ]),
                            ])
                        ]),
                    ])
                ]),
                html.Div(id='forth-content', children=[
                    html.Div(className="card card-stats", children=[
                        html.Div(className="card-body ", children=[
                            html.Div(className='row', children=[
                                html.Div(className="col-5 col-md-4", children=[
                                    html.Div(id='img-content-4', className="icon-big text-center icon-warning")
                                ]),
                                html.Div(className="col-7 col-md-8", children=[
                                    html.Div(className="numbers", children=[
                                        html.P(id='forth-content-1', className="card-category"),
                                        html.P(id='forth-content-2', className="card-title"),
                                    ])
                                ]),
                            ])
                        ]),
                    ])
                ]),
            ]), 
            html.Div(className='row', children=[
                html.Div(className="col-md-4", children=[
                    html.Div(className='card ', children=[
                        html.Div(className='card-header ', children=[
                            html.H5(id='pie-chart-title', className="card-title")
                        ]),
                        html.Div(id='pie-chart-content', className='card-body ', style={'marginTop': -30, 'maxHeight': 500})
                    ])
                ]),
                html.Div(className="col-md-8", children=[
                    html.Div(className='card ', children=[
                        html.Div(className='card-header ', children=[
                            html.H5(id='bar-chart-title', className="card-title", children=['Users Behavior']),
                        ]),
                        html.Div(id='bar-chart', className='card-body ', style={'marginTop': -30, 'maxHeight': 500})
                    ])
                ])
            ]),
            html.Div(className='row', children=[
                html.Div(className="col-md-12", children=[
                    html.Hr(style={'marginBottom': 20})
                ])
            ]),
            html.Div(className='row', children=[
                html.Div(className="col-md-1", children=[
                    html.Div(className="icon-big text-center icon-warning", children=[
                        html.Img(src="./assets/icon/forecast.png", style={'maxHeight': '80px', 'maxWidth': '60px', 'marginTop': 0})
                    ])
                ]),
                html.Div(className="col-md-11", children=[
                    html.H5(children=['Data Forecasting'], style={'fontSize': 25, 'marginTop': 8}),
                ])
            ]),
            html.Div(className='row', children=[
                html.Div(className="col-md-12", children=[
                    html.Hr()
                ])
            ]),
            html.Div(className='row', children=[
                html.Div(className="col-md-12", children=[
                    html.Div(className='card ', children=[
                        html.Div(className='card-header ', children=[
                            html.H5(id='forecast-graph-title', className="card-title"),
                        ]),
                        html.Div(id='forecast-content', className='card-body ')
                    ])
                ])
            ]),
            html.Div(className='row', children=[
                html.Div(className="col-md-12", children=[
                    html.Div(className='card ', children=[
                        html.Div(className='card-header ', children=[
                            html.H5(id='evaluation-graph-title', className="card-title", children=['Model Accuracy Percentage']),
                        ]),
                        html.Div(id='evaluation-content', className='card-body ')
                    ])
                ])
            ]),
        ]),
    ])
])

# Dash app layout
app.layout = html.Div(children=[dcc.Location(id="url"), BODY])

# Dash app callbacks
register_callbacks(app)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8050', debug=True)