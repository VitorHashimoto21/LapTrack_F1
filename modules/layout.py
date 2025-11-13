from dash import dcc, html
from .tabela_pilotos import gerar_tabela_pilotos_sessao

def criar_layout():
    return html.Div(
        style={'backgroundColor': '#000', 'color': 'white', 'padding': '20px'},
        children=[
            # LOGO E TÍTULO
            html.Div([
                html.Img(
                    src="https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg",
                    style={'height': '60px', 'display': 'block', 'margin': '0 auto'}
                ),
                html.H1("LAP TRACK", style={'textAlign': 'center'}),
                html.Div([
                    html.A("⬅ Voltar à Tela Principal", href="/", style={'display': 'block', 'margin': '20px auto', 'width': 'fit-content'})
                ])
            ]),

            # DROPDOWNS
            html.Div([
                html.Div([
                    html.Label("Ano:", style={'color': 'white', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='ano-dropdown',
                        options=[{'label': str(ano), 'value': ano} for ano in range(2021, 2025)],
                        value=2024,
                        style={'backgroundColor': '#111', 'color': 'white'}
                    )
                ], style={'width': '32%', 'display': 'inline-block'}),

                html.Div([
                    html.Label("Corrida:", style={'color': 'white', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='corrida-dropdown',
                        options=[],
                        placeholder="Selecione a corrida",
                        style={'backgroundColor': '#111', 'color': 'white'}
                    )
                ], style={'width': '32%', 'display': 'inline-block', 'paddingLeft': '2%'}),

                html.Div([
                    html.Label("Sessão:", style={'color': 'white', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='sessao-dropdown',
                        options=[
                            {'label': 'Treino Livre 1', 'value': 'FP1'},
                            {'label': 'Treino Livre 2', 'value': 'FP2'},
                            {'label': 'Treino Livre 3', 'value': 'FP3'},
                            {'label': 'Classificação', 'value': 'Q'},
                            {'label': 'Sprint Quali', 'value': 'SQ'},
                            {'label': 'Sprint', 'value': 'S'},
                            {'label': 'Corrida', 'value': 'R'},
                        ],
                        value='R',
                        style={'backgroundColor': '#111', 'color': 'white'}
                    )
                ], style={'width': '32%', 'display': 'inline-block', 'paddingLeft': '2%'}),
            ]),

            html.Br(),

            # PILOTOS
            html.Div([
                html.Div([
                    html.Label("Piloto 1:", style={'color': 'white', 'fontWeight': 'bold'}),
                    dcc.Dropdown(id='piloto1-dropdown', placeholder="Selecione o piloto 1",
                                 style={'backgroundColor': '#111', 'color': 'white'})
                ], style={'width': '49%', 'display': 'inline-block'}),

                html.Div([
                    html.Label("Piloto 2:", style={'color': 'white', 'fontWeight': 'bold'}),
                    dcc.Dropdown(id='piloto2-dropdown', placeholder="Selecione o piloto 2",
                                 style={'backgroundColor': '#111', 'color': 'white'})
                ], style={'width': '49%', 'display': 'inline-block', 'paddingLeft': '2%'}),
            ]),

            html.Br(),
            dcc.Graph(id='grafico-velocidade'),

            html.Br(),

            # MAPA + TABELA
            html.Div(
                style={
                    'backgroundColor': 'black',
                    'color': 'white',
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'alignItems': 'flex-start',
                    'padding': '10px',
                    'gap': '20px'
                },
                children=[
                    html.Div(
                        style={
                            'flex': '1',
                            'display': 'flex',
                            'flexDirection': 'column',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'textAlign': 'center',
                        },
                        children=[
                            html.H2("Mapa do Circuito", style={'color': 'white','textAlign': 'center','marginBottom': '10px'}),
                            html.Div(id='mapa-circuito', style={'display': 'flex','justifyContent': 'center','alignItems': 'center','width': '200%'},
                                     children=[html.P("O mapa do circuito será exibido aqui.", style={'color': 'gray','textAlign': 'center'})])
                        ]
                    ),

                    html.Div(
                        style={'flex': '1','display': 'flex','flexDirection': 'column','alignItems': 'center','justifyContent': 'flex-start','textAlign': 'center'},
                        children=[
                            html.H2("Posições na Sessão", style={'color': 'white'}),
                            html.Div(id='tabela-classificacao', style={'width': '100%'},
                                     children=[gerar_tabela_pilotos_sessao(2024, 'Bahrain', 'R')])
                        ]
                    ),
                ]
            )
        ]
    )