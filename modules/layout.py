from dash import dcc, html
from .git push
tabela_pilotos import gerar_tabela_pilotos_sessao  # importa a função que você já tem

def criar_layout():
    return html.Div(
        style={'backgroundColor': '#000000', 'color': 'white', 'padding': '20px'},
        children=[

            # ======== LOGO E TÍTULO PRINCIPAL ========
            html.Div([
                html.Img(
                    src="https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg",
                    style={'height': '60px', 'display': 'block', 'margin': '0 auto'}
                )
            ]),
            html.H1("LAP TRACK", style={'textAlign': 'center'}),

            # ======== DROPDOWNS DE FILTRO ========
            html.Div([
                html.Div([
                    html.Label("Ano:", style={'color': 'white'}),
                    dcc.Dropdown(
                        id='ano-dropdown',
                        options=[{'label': str(ano), 'value': ano} for ano in range(2021, 2025)],
                        value=2024,
                        style={'backgroundColor': 'white', 'color': 'black'}
                    )
                ], style={'width': '32%', 'display': 'inline-block'}),

                html.Div([
                    html.Label("Corrida:", style={'color': 'white'}),
                    dcc.Dropdown(
                        id='corrida-dropdown',
                        options=[],
                        style={'backgroundColor': 'white', 'color': 'black'}
                    )
                ], style={'width': '32%', 'display': 'inline-block', 'paddingLeft': '2%'}),

                html.Div([
                    html.Label("Sessão:", style={'color': 'white'}),
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
                        style={'backgroundColor': 'white', 'color': 'black'}
                    )
                ], style={'width': '32%', 'display': 'inline-block', 'paddingLeft': '2%'}),
            ]),

            html.Br(),

            # ======== SELEÇÃO DE PILOTOS ========
            html.Div([
                html.Div([
                    html.Label("Piloto 1:", style={'color': 'white'}),
                    dcc.Dropdown(id='piloto1-dropdown', style={'backgroundColor': 'white', 'color': 'black'})
                ], style={'width': '49%', 'display': 'inline-block'}),

                html.Div([
                    html.Label("Piloto 2:", style={'color': 'white'}),
                    dcc.Dropdown(id='piloto2-dropdown', style={'backgroundColor': 'white', 'color': 'black'})
                ], style={'width': '49%', 'display': 'inline-block', 'paddingLeft': '2%'}),
            ]),

            html.Br(),
            dcc.Graph(id='grafico-velocidade'),

            html.Br(),

            # ======== MAPA + CLASSIFICAÇÃO (LADO A LADO) ========
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
                    # ---- Coluna do MAPA ----
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
                            html.H2("Mapa do Circuito", style={
                                'color': 'white',
                                'textAlign': 'center',
                                'marginBottom': '10px'
                            }),
                            html.Div(
                                id='mapa-circuito',
                                style={
                                    'display': 'flex',
                                    'justifyContent': 'center',
                                    'alignItems': 'center',
                                    'width': '200%'
                                },
                                children=[
                                    html.P(
                                        "O mapa do circuito será exibido aqui.",
                                        style={'color': 'gray', 'textAlign': 'center'}
                                    )
                                ]
                            )
                        ]
                    ),

                    # ---- Coluna da CLASSIFICAÇÃO ----
                    html.Div(
                        style={
                            'flex': '1',
                            'display': 'flex',
                            'flexDirection': 'column',
                            'alignItems': 'center',
                            'justifyContent': 'flex-start',
                            'textAlign': 'center'
                        },
                        children=[
                            html.H2("Classificação da Sessão", style={'color': 'white'}),

                            # === Aqui a tabela é chamada diretamente ===
                            html.Div(
                                id='tabela-classificacao',
                                style={'width': '100%'},
                                children=[
                                    gerar_tabela_pilotos_sessao(2024, 'Bahrain', 'R')
                                    # você pode alterar os valores fixos acima ou ligá-los a callbacks
                                ]
                            )
                        ]
                    ),
                ]
            )
        ]
    )
