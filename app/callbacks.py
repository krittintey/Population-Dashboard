import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from data import df_visualize, df_popData, last_modified_update
from forecast import createForecastDataframe, modelEvaluation
import numpy as np

def register_callbacks(app):

    # URL callback
    @app.callback(
        [Output(f"page-{i}-link", "className") for i in range(1, 4)],
        [Input("url", "pathname")],
    )
    def toggle_active_links(pathname):
        if (pathname == "/") | (pathname == "/population"):
            return 'active', '', ''
        elif pathname == "/births":
            return '', 'active', ''
        elif pathname == "/deaths":
            return '', '', 'active'
        else:
            return '', '', ''

    # Overall graph callback
    @app.callback([Output("first-graph", "children"), Output("graph-title", "children")], [Input("url", "pathname")])
    def render_overall_graph(pathname):
        if pathname in ["/", "/population"]:
            first_graph = dcc.Graph(id='first-graph', figure={
                'data': df_visualize[0],
                'layout': go.Layout(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    autosize=True,
                    hovermode='x',
                    xaxis={'autorange': True, 'showspikes': True, 'spikemode': 'toaxis'},
                    yaxis={'autorange': True, 'showspikes': True, 'spikemode': 'toaxis'}
                )
            }, config=dict(responsive=True))
            return first_graph, 'Thai Population (1998-2019)'
        elif pathname == "/births":
            first_graph = dcc.Graph(id='birth-first-graph', figure={
                'data': df_visualize[1],
                'layout': go.Layout(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    autosize=True,
                    hovermode='x',
                    xaxis={'autorange': True, 'showspikes': True, 'spikemode': 'toaxis'},
                    yaxis={'autorange': True, 'showspikes': True, 'spikemode': 'toaxis'}
                )
            }, config=dict(responsive=True))
            return first_graph, 'Thai Births (1998-2019)'
        elif pathname == "/deaths":
            first_graph = dcc.Graph(id='death-first-graph', figure={
                'data': df_visualize[2],
                'layout': go.Layout(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    autosize=True,
                    hovermode='x',
                    xaxis={'autorange': True, 'showspikes': True, 'spikemode': 'toaxis'},
                    yaxis={'autorange': True, 'showspikes': True, 'spikemode': 'toaxis'}
                )
            }, config=dict(responsive=True))
            return first_graph, 'Thai Deaths (1998-2019)'
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognized..."),
            ],
        ), None
    
    # Callback for showing the layout of the first report content
    @app.callback(Output("first-content", "children"), [Input("url", "pathname")])
    def render_first_content(pathname):
        if pathname in ["/", "/population"]:
            first_content = [html.Div(className="card card-stats", children=[
                        html.Div(className="card-body ", children=[
                            html.Div(className='row', children=[
                                html.Div(className="col-5 col-md-4", children=[
                                    html.Div(id='img-content-1', className="icon-big text-center icon-warning", children=[
                                        #html.I(className="nc-icon nc-globe text-warning")
                                        html.Img(src="./assets/images/team.png", style={'maxHeight': '80px', 'maxWidth': '60px', 'marginTop': -8})
                                    ])
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
                ]
            return first_content
        return [html.P(id='first-content-1', className="card-category"), html.P(id='first-content-2', className="card-title")]

    # Callbacks for all contents
    @app.callback(
        [Output("first-content", "className"), Output("second-content", "className"), Output("third-content", "className"), Output("forth-content", "className"), 
        Output("first-content-1", "children"), Output("first-content-2", "children"), Output("second-content-1", "children"), Output("second-content-2", "children"),
        Output("third-content-1", "children"), Output("third-content-2", "children"), Output("forth-content-1", "children"), Output("forth-content-2", "children")],
        [Input("url", "pathname"), Input("year-dropdown", "value"), Input("month-dropdown", "value")]
    )
    def update_content(pathname, year, month):
        year_month = f'{year}-{month}'

        if pathname in ["/", "/population"]:
            content1 = f"Thai Total Population in {year_month}"
            content2 = f"Thai Male Population in {year_month}"
            content3 = f"Thai Female Population in {year_month}"
            content4 = f"Thai House Population in {year_month}"

            pop = "{:,}".format(df_popData['POP_MALE'][str(year_month)].values[0] + df_popData['POP_FEMALE'][str(year_month)].values[0])
            male = "{:,}".format(df_popData['POP_MALE'][str(year_month)].values[0])
            female = "{:,}".format(df_popData['POP_FEMALE'][str(year_month)].values[0])
            house = "{:,}".format(df_popData['HOUSE'][str(year_month)].values[0])

            class_content = "col-lg-3 col-md-6 col-sm-6"

            return class_content, class_content, class_content, class_content, content1, pop, content2, male, content3, female, content4, house
        elif pathname == "/births":
            content1 = f"Thai Total Births in {year_month}"
            content2 = f"Thai Male Births in {year_month}"
            content3 = f"Thai Female Births in {year_month}"

            pop = "{:,}".format(df_popData['BIRTH_MALE'][str(year_month)].values[0] + df_popData['BIRTH_FEMALE'][str(year_month)].values[0])
            male = "{:,}".format(df_popData['BIRTH_MALE'][str(year_month)].values[0])
            female = "{:,}".format(df_popData['BIRTH_FEMALE'][str(year_month)].values[0])

            class_content = "col-lg-4 col-md-6 col-sm-6"

            return "", class_content, class_content, class_content, None, None, content1, pop, content2, male, content3, female
        elif pathname == "/deaths":
            content1 = f"Thai Total Deaths in {year_month}"
            content2 = f"Thai Male Deaths in {year_month}"
            content3 = f"Thai Female Deaths in {year_month}"

            pop = "{:,}".format(df_popData['DEATH_MALE'][str(year_month)].values[0] + df_popData['DEATH_FEMALE'][str(year_month)].values[0])
            male = "{:,}".format(df_popData['DEATH_MALE'][str(year_month)].values[0])
            female = "{:,}".format(df_popData['DEATH_FEMALE'][str(year_month)].values[0])

            class_content = "col-lg-4 col-md-6 col-sm-6"
            
            return "", class_content, class_content, class_content, None, None, content1, pop, content2, male, content3, female
        return "", "", "", "", None, None, None, None, None, None, None, None

    # Callback for the content images
    @app.callback([Output("img-content-2", "children"), Output("img-content-3", "children"), Output("img-content-4", "children")], [Input("url", "pathname")])
    def render_image_content(pathname):
        if pathname in ["/", "/population"]:
            img1 = html.Img(src="./assets/images/male.png", style={'maxHeight': '80px', 'maxWidth': '60px', 'marginTop': -8})
            img2 = html.Img(src="./assets/images/female.png", style={'maxHeight': '80px', 'maxWidth': '60px', 'marginTop': -8})
            img3 = html.Img(src="./assets/images/home.png", style={'maxHeight': '80px', 'maxWidth': '60px', 'marginTop': -8})

            return img1, img2, img3
        elif pathname == "/births":
            img1 = html.Img(src="./assets/images/children.png", style={'maxHeight': '80px', 'maxWidth': '60px', 'marginTop': -8})
            img2 = html.Img(src="./assets/images/male_children.png", style={'maxHeight': '80px', 'maxWidth': '60px', 'marginTop': -8})
            img3 = html.Img(src="./assets/images/female_children.png", style={'maxHeight': '80px', 'maxWidth': '60px', 'marginTop': -8})
            
            return img1, img2, img3
        elif pathname == "/deaths":
            img1 = html.Img(src="./assets/images/death.png", style={'maxHeight': '80px', 'maxWidth': '60px', 'marginTop': -8})
            img2 = html.Img(src="./assets/images/oldmale.png", style={'maxHeight': '80px', 'maxWidth': '60px', 'marginTop': -8})
            img3 = html.Img(src="./assets/images/oldfemale.png", style={'maxHeight': '80px', 'maxWidth': '60px', 'marginTop': -8})
            
            return img1, img2, img3
        return None, None, None

    # Callback for updating pie chart
    @app.callback([Output("pie-chart-content", "children"), Output("pie-chart-title", "children")], [Input("url", "pathname"), Input("year-dropdown", "value"), Input("month-dropdown", "value")])
    def update_pie_chart(pathname, year, month):
        year_month = f'{year}-{month}'

        if pathname in ["/", "/population"]:
            male = df_popData['POP_MALE'][str(year_month)].values[0]
            female = df_popData['POP_FEMALE'][str(year_month)].values[0]

            figure={
                'data': [go.Pie(
                    labels=['Male', 'Female'], 
                    values=[male, female], 
                    textinfo='label+percent', 
                    hole=.5, 
                    textfont_size=15, 
                    marker=dict(line=dict(color='#000000', width=1.5)),
                    opacity=0.9
                )],
                'layout': go.Layout(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    height=400,
                    hovermode='x',
                    xaxis={'autorange': True},
                    yaxis={'autorange': True}
                )
            }

            title=f'Thai Population Ratio in {year_month}'

            return dcc.Graph(id='pie-chart', figure=figure), title
        elif pathname == "/births":
            male = df_popData['BIRTH_MALE'][str(year_month)].values[0]
            female = df_popData['BIRTH_FEMALE'][str(year_month)].values[0]
            
            figure={
                'data': [go.Pie(
                    labels=['Male', 'Female'], 
                    values=[male, female], 
                    textinfo='label+percent', 
                    hole=.5, 
                    textfont_size=15, 
                    marker=dict(line=dict(color='#000000', width=1.5)),
                    opacity=0.9
                )],
                'layout': go.Layout(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    height=400,
                    hovermode='x',
                    xaxis={'autorange': True},
                    yaxis={'autorange': True}
                )
            }

            title=f'Thai Birth Ratio in {year_month}'

            return dcc.Graph(id='pie-chart', figure=figure), title
        elif pathname == "/deaths":
            male = df_popData['DEATH_MALE'][str(year_month)].values[0]
            female = df_popData['DEATH_FEMALE'][str(year_month)].values[0]
            
            figure={
                'data': [go.Pie(
                    labels=['Male', 'Female'], 
                    values=[male, female], 
                    textinfo='label+percent', 
                    hole=.5, 
                    textfont_size=15, 
                    marker=dict(line=dict(color='#000000', width=1.5)),
                    opacity=0.9
                )],
                'layout': go.Layout(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    height=400,
                    hovermode='x',
                    xaxis={'autorange': True},
                    yaxis={'autorange': True}
                )
            }

            title=f'Thai Death Ratio in {year_month}'

            return dcc.Graph(id='pie-chart', figure=figure), title
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognized..."),
            ],
        ), None

    # Callback for updating bar chart content
    @app.callback([Output("bar-chart", "children"), Output("bar-chart-title", "children")], [Input("url", "pathname"), Input("year-dropdown", "value"), Input("month-dropdown", "value")])
    def update_bar_chart(pathname, year, month):
        year_month = f'{year}-{month}'

        if pathname in ["/", "/population"]:
            total = df_popData['POP_MALE'][str(year_month)].values[0] + df_popData['POP_FEMALE'][str(year_month)].values[0]
        
            figure = go.Figure(
                data=[
                    go.Bar(
                        x=['MALE', 'FEMALE', 'HOUSE', 'TOTAL'], 
                        y=np.append(df_popData[df_popData.columns[0:3]][year_month].values[0], total),
                        text=np.append(df_popData[df_popData.columns[0:3]][year_month].values[0], total)
                    )
                ],
                layout=dict(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    height=400,
                    xaxis={'autorange': True},
                    yaxis={'autorange': True}
                )
            )
            figure.update_traces(
                marker_line_color='rgb(8,48,107)', 
                marker_line_width=1.5, 
                opacity=0.8,
                texttemplate='%{text:.2s}', 
                textposition='inside'
            )

            title=f'Thai Population Bar Chart in {year_month}'

            return dcc.Graph(id='forecast-graph', figure=figure), title
        elif pathname == "/births":
            total = df_popData['BIRTH_MALE'][str(year_month)].values[0] + df_popData['BIRTH_FEMALE'][str(year_month)].values[0]
            
            figure = go.Figure(
                data=[
                    go.Bar(
                        x=['MALE', 'FEMALE', 'TOTAL'], 
                        y=np.append(df_popData[df_popData.columns[3:5]][year_month].values[0], total),
                        text=np.append(df_popData[df_popData.columns[3:5]][year_month].values[0], total)
                    )
                ],
                layout=dict(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    height=400,
                    xaxis={'autorange': True},
                    yaxis={'autorange': True}
                )
            )
            figure.update_traces(
                marker_line_color='rgb(8,48,107)', 
                marker_line_width=1.5, 
                opacity=0.8,
                texttemplate='%{text:.2s}', 
                textposition='inside'
            )

            title=f'Thai Birth Bar Chart in {year_month}'

            return dcc.Graph(id='forecast-graph', figure=figure), title
        elif pathname == "/deaths":
            total = df_popData['DEATH_MALE'][str(year_month)].values[0] + df_popData['DEATH_FEMALE'][str(year_month)].values[0]
            
            figure = go.Figure(
                data=[
                    go.Bar(
                        x=['MALE', 'FEMALE', 'TOTAL'], 
                        y=np.append(df_popData[df_popData.columns[5:7]][year_month].values[0], total),
                        text=np.append(df_popData[df_popData.columns[5:7]][year_month].values[0], total)
                    )
                ],
                layout=dict(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    height=400,
                    xaxis={'autorange': True},
                    yaxis={'autorange': True}
                )
            )
            figure.update_traces(
                marker_line_color='rgb(8,48,107)', 
                marker_line_width=1.5, 
                opacity=0.8,
                texttemplate='%{text:.2s}', 
                textposition='inside'
            )

            title=f'Thai Death Bar Chart in {year_month}'

            return dcc.Graph(id='forecast-graph', figure=figure), title
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognized..."),
            ],
        ), None

    # Callback for updating forecasted content
    @app.callback([Output("forecast-content", "children"), Output("forecast-graph-title", "children"), Output("evaluation-content", "children")], [Input("url", "pathname")])
    def update_forecast_graph(pathname):
        if pathname in ["/", "/population"]:
            df_predict, df_forecast = createForecastDataframe(df_popData[df_popData.columns[0:3]], last_modified_update)
            rmspe = modelEvaluation(df_popData[df_popData.columns[0:3]], df_predict)

            df_forecast_visualize = list()
            df_male = dict(x=df_forecast.index, y=df_forecast['POP_MALE'], name='Forecasted Male', type='line')
            df_female = dict(x=df_forecast.index, y=df_forecast['POP_FEMALE'], name='Forecasted Female', type='line')
            df_total = dict(x=df_forecast.index, y=df_forecast['POP_MALE'] + df_forecast['POP_FEMALE'], name='Forecasted Total', type='line')
            df_house = dict(x=df_forecast.index, y=df_forecast['HOUSE'], name='Forecasted House', type='line')
            df_forecast_visualize = [df_male, df_female, df_house, df_total]

            figure1 = {
                'data': df_forecast_visualize,
                'layout': go.Layout(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    height=400,
                    hovermode='x',
                    xaxis={'autorange': True, 'showspikes': True, 'spikemode': 'toaxis'},
                    yaxis={'autorange': True, 'showspikes': True, 'spikemode': 'toaxis'}
                )
            }

            title=f'Thai Population Forecasting (Next 3 Year)'

            figure2 = go.Figure(
                data=[
                    go.Bar(
                        x=['MALE', 'FEMALE', 'HOUSE'], 
                        y=rmspe,
                        text=rmspe
                    )
                ],
                layout=dict(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    height=400,
                    xaxis={'autorange': True},
                    yaxis={'autorange': True}
                )
            )

            figure2.update_traces(
                marker_color='rgb(0,201,53)', 
                marker_line_color='rgb(0,108,29)', 
                marker_line_width=1.5, 
                opacity=0.8,
                texttemplate='%{text:.3f}%', 
                textposition='inside'
            )

            return dcc.Graph(id='forecast-graph', figure=figure1), title, dcc.Graph(id='evaluation-graph', figure=figure2)
        elif pathname == "/births":
            df_predict, df_forecast = createForecastDataframe(df_popData[df_popData.columns[3:5]], last_modified_update)
            rmspe = modelEvaluation(df_popData[df_popData.columns[3:5]], df_predict)

            df_forecast_visualize = list()
            df_male = dict(x=df_forecast.index, y=df_forecast['BIRTH_MALE'], name='Forecasted Male', type='line')
            df_female = dict(x=df_forecast.index, y=df_forecast['BIRTH_FEMALE'], name='Forecasted Female', type='line')
            df_total = dict(x=df_forecast.index, y=df_forecast['BIRTH_MALE'] + df_forecast['BIRTH_FEMALE'], name='Forecasted Total', type='line')
            df_forecast_visualize = [df_male, df_female, df_total]

            figure1 = {
                'data': df_forecast_visualize,
                'layout': go.Layout(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    height=400,
                    hovermode='x',
                    xaxis={'autorange': True, 'showspikes': True, 'spikemode': 'toaxis'},
                    yaxis={'autorange': True, 'showspikes': True, 'spikemode': 'toaxis'}
                )
            }

            title=f'Thai Birth Forecasting (Next 3 Year)'

            figure2 = go.Figure(
                data=[
                    go.Bar(
                        x=['MALE', 'FEMALE'], 
                        y=rmspe,
                        text=rmspe
                    )
                ],
                layout=dict(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    height=400,
                    xaxis={'autorange': True},
                    yaxis={'autorange': True}
                )
            )

            figure2.update_traces(
                marker_color='rgb(0,201,53)', 
                marker_line_color='rgb(0,108,29)', 
                marker_line_width=1.5, 
                opacity=0.8,
                texttemplate='%{text:.3f}%', 
                textposition='inside'
            )

            return dcc.Graph(id='forecast-graph', figure=figure1), title, dcc.Graph(id='forecast-graph', figure=figure2)
        elif pathname == "/deaths":
            df_predict, df_forecast = createForecastDataframe(df_popData[df_popData.columns[5:7]], last_modified_update)
            rmspe = modelEvaluation(df_popData[df_popData.columns[5:7]], df_predict)

            df_forecast_visualize = list()
            df_male = dict(x=df_forecast.index, y=df_forecast['DEATH_MALE'], name='Forecasted Male', type='line')
            df_female = dict(x=df_forecast.index, y=df_forecast['DEATH_FEMALE'], name='Forecasted Female', type='line')
            df_total = dict(x=df_forecast.index, y=df_forecast['DEATH_MALE'] + df_forecast['DEATH_FEMALE'], name='Forecasted Total', type='line')
            df_forecast_visualize = [df_male, df_female, df_total]
            
            figure1 = {
                'data': df_forecast_visualize,
                'layout': go.Layout(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    height=400,
                    hovermode='x',
                    xaxis={'autorange': True, 'showspikes': True, 'spikemode': 'toaxis'},
                    yaxis={'autorange': True, 'showspikes': True, 'spikemode': 'toaxis'}
                )
            }

            title=f'Thai Death Forecasting (Next 3 Year)'
            
            figure2 = go.Figure(
                data=[
                    go.Bar(
                        x=['MALE', 'FEMALE'], 
                        y=rmspe,
                        text=rmspe
                    )
                ],
                layout=dict(
                    template='plotly_white',
                    font=dict(family='Ubuntu'),
                    height=400,
                    xaxis={'autorange': True},
                    yaxis={'autorange': True}
                )
            )

            figure2.update_traces(
                marker_color='rgb(0,201,53)', 
                marker_line_color='rgb(0,108,29)', 
                marker_line_width=1.5, 
                opacity=0.8,
                texttemplate='%{text:.3f}%', 
                textposition='inside'
            )

            return dcc.Graph(id='forecast-graph', figure=figure1), title, dcc.Graph(id='forecast-graph', figure=figure2)
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognized..."),
            ],
        ), None, None
