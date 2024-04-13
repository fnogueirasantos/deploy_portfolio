from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Define the layout of the app

style_card = style={'width': '70%', 'backgroundColor': '#1c1e1c', 'color':'#fefdfd'}

def create_layout():
    return dbc.Container(
        fluid=True,
        style={'backgroundColor': '#1e0000'},
        children=[
            html.Br(),
            html.A(html.Button('Back'), href='/index', style={'position': 'absolute', 'top': 5, 'left': 10}),
            html.A(
                html.H3('Dashboard - Finance and Controlling'),
                style={
                    'position': 'absolute',
                    'top': 3,
                    'left': 100,
                    'color': 'white',
                    'font-family': 'Arial',
                }
            ),
            html.Br(),
            dcc.Tabs(
                id='tabs',
                value='tab_1',
                className='dbc',
                style={
                    'fontFamily': 'Arial, sans-serif',
                    'border': '10px solid #ddd',
                    'borderRadius': '4px',
                    'padding': '10px',
                    'backgroundColor': '#f8f9fa',
                    'width': '50%',  # Adjust the width as needed
                    'maxWidth': '1200px',  # Set the maximum width if desired
                    'margin': 'auto',  # Center the tabs horizontally
                },
                children=[
                    dcc.Tab(
                        label='General Overview',
                        value='tab_1',
                        className='dbc',
                        children=[
                            html.Br(),
                            dbc.Row([
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(id="card1"),
                                        style=style_card, className="border-0"
                                    )
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(id="card2"),
                                        style=style_card, className="border-0"
                                    )
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(id="card3"),
                                        style=style_card, className="border-0"
                                    )
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(id="card4"),
                                        style=style_card, className="border-0"
                                    )
                                ),
                            ], style={'backgroundColor': '#1c1e1c'}
                            ),
                            html.Br(),
                            dcc.Dropdown(
                                id='filter_dre',
                                options=['(+) Gross Revenue', '(-) Deductions', '(=) Net Revenue',
                                        '(-) Cost of Goods/Services', '(=) Gross Profit',
                                        '(-) Personnel Expenses', '(-) Administrative Expenses',
                                        '(-) IT Expenses', '(-) Marketing and Sales Expenses',
                                        '(-) General Expenses', '(=) EBITDA', '(+) Financial Charges',
                                        '(-) Financial Income', '(-) Profit Tax',
                                        '(-) Depreciation / Amortization', '(=) Net Result'],
                                value='(+) Gross Revenue',
                                clearable=False,
                                style={'width': '50%', 'margin': 'auto'}  # Center horizontally
                            ),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(dbc.Card(dcc.Graph(id='barchart_value',
                                                        config={'displayModeBar': False})), width=6),
                                dbc.Col(dbc.Card(dcc.Graph(id='barchart_percentage',
                                                        config={'displayModeBar': False}
                                                        )), width=6)
                            ]),
                            html.Hr(),
                            dbc.Row([
                                dbc.Col(dbc.Card(dcc.Graph(id='waterfall_company',
                                                        config={'displayModeBar': False})), width=8, style={'margin': '0 auto'}),
                            ]),
                            html.Br(),
                        ],
                    ),
                    dcc.Tab(
                        label="Statement of Income",
                        value="tab-2",
                        children=[
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        children=[
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(
                                                        [
                                                            html.H6("Statement of Income for the year"),
                                                            html.Div(
                                                                [
                                                                    html.Label("Select Filter"),
                                                                    dcc.Dropdown(
                                                                        id='filter_company',
                                                                        options=[
                                                                            {'label': 'Consolidated', 'value': 'Consolidated'},
                                                                            {'label': 'Aesthetics', 'value': 'Aesthetics'},
                                                                            {'label': 'Building Material Store',
                                                                            'value': 'Building Material Store'},
                                                                            {'label': 'Clothes Store', 'value': 'Clothes Store'},
                                                                            {'label': 'Drug Store', 'value': 'Drug Store'},
                                                                            {'label': 'Goods Store', 'value': 'Goods Store'},
                                                                        ],
                                                                        value='Consolidated',
                                                                        clearable=False,
                                                                    ),
                                                                    html.Hr(),
                                                                    dcc.RadioItems(
                                                                        id='filter_resume',
                                                                        options=[
                                                                            {'label': 'Resume', 'value': 'Resume'},
                                                                            {'label': 'Complete', 'value': 'Complete'},
                                                                        ],
                                                                        value='Resume'
                                                                    ),
                                                                ],
                                                                className="mr-3",
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.CardBody(
                                                        dash_table.DataTable(
                                                            id='dre_table',
                                                            style_table={'height': '220px', 'overflowY': 'auto'},
                                                            style_as_list_view=True,
                                                            style_cell={'textAlign': 'left',
                                                                        'overflow': 'hidden',
                                                                        'textOverflow': 'ellipsis',},
                                                            style_header={
                                                                'backgroundColor': '#1c1e1c',
                                                                'fontWeight': 'bold',
                                                                'color' : 'white'
                                                            },
                                                            style_data={ 'border': '1px solid #1c1e1c' },
                                                            export_format='xlsx',
                                                        ),
                                                    ),
                                                ],
                                                body=True
                                            )
                                        ],
                                        width=6
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dcc.Graph(id='waterfall_dre',config={'displayModeBar': False}),
                                            body=True,
                                            style={'height': '500px'}  # Set the height of the dbc.Card
                                        ),
                                        width=6,
                                        style={'height': '500px'}  # Set the height of the dbc.Col
                                    ),
                                ]
                            ),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        children=[
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(
                                                        [
                                                            html.H6("Statement of Income for the year"),
                                                            html.Div([
                                                                html.Label("Select Filter"),
                                                                dcc.Dropdown(
                                                                    id='filter_sub_account',
                                                                    options=[
                                                                        {'label': '(+) Gross Revenue',
                                                                        'value': '(+) Gross Revenue'},
                                                                        {'label': '(-) Cost of Goods/Services',
                                                                        'value': '(-) Cost of Goods/Services'},
                                                                        {'label': '(-) Personnel Expenses',
                                                                        'value': '(-) Personnel Expenses'},
                                                                        {'label': '(-) Administrative Expenses',
                                                                        'value': '(-) Administrative Expenses'},
                                                                        {'label': '(-) IT Expenses', 'value': '(-) IT Expenses'},
                                                                        {'label': '(-) General Expenses',
                                                                        'value': '(-) General Expenses'}
                                                                    ],
                                                                    value='(+) Gross Revenue',
                                                                    clearable=False,
                                                                )
                                                            ]
                                                            )
                                                        ]
                                                    ),
                                                    dbc.CardBody(
                                                        dash_table.DataTable(
                                                            id='sub_account_table',
                                                            style_table={'height': '312px', 'overflowY': 'auto'},
                                                            style_as_list_view=True,
                                                            style_cell={'textAlign': 'left',
                                                                        'overflow': 'hidden',
                                                                        'textOverflow': 'ellipsis',},
                                                            style_header={
                                                                'backgroundColor': '#1c1e1c',
                                                                'fontWeight': 'bold',
                                                                'color' : 'white'
                                                            },
                                                            style_data={ 'border': '1px solid #1c1e1c' },
                                                            export_format='xlsx',
                                                        ),
                                                    ),
                                                ],
                                                body=False
                                            )
                                        ],
                                        width=6
                                    ),
                                    dbc.Col(dbc.Card(dcc.Graph(id='water_fall_sub_account',config={'displayModeBar': False}),
                                                    body=True,
                                                    style={'height': '480px'}),
                                                    width=6),
                                ]
                            ),html.Br(),
                        ],
                    ),
                ]
            ),
        ]
    )