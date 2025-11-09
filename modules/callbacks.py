from dash import Input, Output, html
from assets import utils
import plotly.graph_objs as go
import fastf1
import pandas as pd
from utils import cores_equipes
from track_map import gerar_mapa_comparativo
from tabela_pilotos import gerar_tabela_pilotos_sessao


def registrar_callbacks(app):

    # Atualiza as corridas
    @app.callback(
        Output('corrida-dropdown', 'options'),
        Input('ano-dropdown', 'value')
    )
    def atualizar_corridas(ano):
        try:
            eventos = fastf1.get_event_schedule(ano)
            return [{'label': f"{row['EventName']} ({row['Country']})", 'value': row['RoundNumber']} for _, row in eventos.iterrows()]
        except:
            return []

    # Atualiza os pilotos
    @app.callback(
        [Output('piloto1-dropdown', 'options'),
         Output('piloto1-dropdown', 'value'),
         Output('piloto2-dropdown', 'options'),
         Output('piloto2-dropdown', 'value')],
        [Input('ano-dropdown', 'value'),
         Input('corrida-dropdown', 'value'),
         Input('sessao-dropdown', 'value')]
    )
    def atualizar_pilotos(ano, round_num, sessao):
        try:
            sessao_f1 = fastf1.get_session(ano, round_num, sessao)
            sessao_f1.load()
            laps = sessao_f1.laps
            pilotos_e_equipes = laps[['Driver', 'Team']].drop_duplicates()
            pilotos_e_equipes['label'] = pilotos_e_equipes.apply(lambda x: f"{x['Driver']} ({x['Team']})", axis=1)
            pilotos_e_equipes['value'] = pilotos_e_equipes['Driver']
            opcoes = pilotos_e_equipes[['label', 'value']].to_dict('records')
            valores = pilotos_e_equipes['value'].tolist()
            return opcoes, valores[0], opcoes, valores[1] if len(valores) > 1 else valores[0]
        except:
            return [], None, [], None

    # Callback do gráfico de velocidade
    @app.callback(
        Output('grafico-velocidade', 'figure'),
        [Input('ano-dropdown', 'value'),
         Input('corrida-dropdown', 'value'),
         Input('sessao-dropdown', 'value'),
         Input('piloto1-dropdown', 'value'),
         Input('piloto2-dropdown', 'value')]
    )
    def atualizar_grafico(ano, round_num, sessao, piloto1, piloto2):
        fig = go.Figure()
        try:
            sessao_f1 = fastf1.get_session(ano, round_num, sessao)
            sessao_f1.load()
            volta1 = sessao_f1.laps.pick_driver(piloto1).pick_fastest()
            volta2 = sessao_f1.laps.pick_driver(piloto2).pick_fastest()
            tel1 = volta1.get_car_data().add_distance()
            tel2 = volta2.get_car_data().add_distance()
            fig.add_trace(go.Scatter(
                x=tel1['Distance'], y=tel1['Speed'],
                mode='lines', name=piloto1,
                line=dict(color=cores_equipes.get(piloto1, 'white'))
            ))

            fig.add_trace(go.Scatter(
                x=tel2['Distance'], y=tel2['Speed'],
                mode='lines', name=piloto2,
                line=dict(color=cores_equipes.get(piloto2, 'gray'))
            ))
            fig.update_layout(
                title=f"Velocidade nas voltas mais rápidas - {piloto1} vs {piloto2}",
                xaxis_title='Distância (m)',
                yaxis_title='Velocidade (km/h)',
                template='plotly_dark'
            )
        except:
            fig.update_layout(
                title="Erro ao carregar dados. Verifique se a sessão existe.",
                template='plotly_dark'
            )
        return fig

    # ✅ Callback do mapa comparativo
    @app.callback(
        Output('mapa-circuito', 'children'),
        [Input('ano-dropdown', 'value'),
         Input('corrida-dropdown', 'value'),
         Input('sessao-dropdown', 'value'),
         Input('piloto1-dropdown', 'value'),
         Input('piloto2-dropdown', 'value')]
    )
    def atualizar_mapa_callback(ano, corrida, sessao, piloto1, piloto2):
        try:
            img_src = gerar_mapa_comparativo(corrida, ano, piloto1, piloto2, sessao)
            if img_src:
                return html.Img(
                    src=img_src,
                    style={
                        'width': '50%',
                        'borderRadius': '12px',
                        'display': 'block',
                        'marginLeft': '0%',
                        'marginTop': '10px',
                    }
                )
            else:
                return html.P("Erro ao gerar mapa.", style={'color': 'red'})
        except Exception as e:
            return html.P(f"Erro: {e}", style={'color': 'red'})

    # ✅ Callback da tabela de pilotos (melhor volta + composto)
    @app.callback(
        Output('tabela-classificacao', 'children'),
        [Input('ano-dropdown', 'value'),
        Input('corrida-dropdown', 'value'),
        Input('sessao-dropdown', 'value')]
    )

    def atualizar_tabela_pilotos(ano, corrida, sessao):
        if not ano or not corrida or not sessao:
            return html.P("Selecione ano, corrida e sessão.", style={"color": "yellow"})
        try:
            return gerar_tabela_pilotos_sessao(ano, corrida, sessao)
        except Exception as e:
            return html.P(f"Erro ao gerar tabela: {e}", style={"color": "red"})
