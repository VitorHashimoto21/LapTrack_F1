from dash import html
import fastf1
import pandas as pd

# 🎨 Cores oficiais das equipes
CORES_EQUIPES = {
    'Red Bull': '#1E41FF',
    'Ferrari': '#DC0000',
    'Mercedes': '#00D2BE',
    'McLaren': '#FF8700',
    'Aston Martin': '#006F62',
    'Alpine': '#0090FF',
    'AlphaTauri RB': '#2B4562',
    'Williams': '#005AFF',
    'Sauber': '#00E701',
    'Haas': '#B6BABD',
}

# 🏎️ Normalização de nomes
NOMES_EQUIPES_NORMALIZADOS = {
    'Red Bull Racing': 'Red Bull',
    'Oracle Red Bull Racing': 'Red Bull',
    'Mercedes-AMG Petronas Formula One Team': 'Mercedes',
    'Scuderia Ferrari': 'Ferrari',
    'McLaren F1 Team': 'McLaren',
    'Aston Martin Aramco Cognizant F1 Team': 'Aston Martin',
    'BWT Alpine F1 Team': 'Alpine',
    'Alpine F1 Team': 'Alpine',
    'RB F1 Team': 'AlphaTauri RB',
    'Visa Cash App RB': 'AlphaTauri RB',
    'Scuderia AlphaTauri': 'AlphaTauri RB',
    'Williams Racing': 'Williams',
    'Alfa Romeo F1 Team Stake': 'Sauber',
    'Kick Sauber': 'Sauber',
    'Stake F1 Team Kick Sauber': 'Sauber',
    'Haas F1 Team': 'Haas',
}


def gerar_tabela_pilotos_sessao(ano, corrida, sessao):
    """
    Gera tabela com posição, equipe, piloto, melhor volta e composto de pneu.
    Compatível com FP1/FP2/FP3, Quali e Corrida.
    """
    try:
        # 🔹 Carregar sessão
        session = fastf1.get_session(ano, corrida, sessao)
        session.load(laps=True, telemetry=False)

        laps = session.laps
        if laps is None or laps.empty:
            return html.Div("⚠️ Nenhum dado de volta encontrado.", style={'color': 'white'})

        # 🔹 Filtrar voltas válidas
        laps = laps[laps['LapTime'].notnull()].copy()
        if laps.empty:
            return html.Div("⚠️ Nenhum tempo de volta válido.", style={'color': 'white'})

        # 🔹 Melhor volta por piloto
        melhores_voltas = laps.groupby('Driver')['LapTime'].min().sort_values().reset_index()

        # 🔹 Pegar equipe e composto do pneu
        def pegar_info_piloto(driver):
            piloto_laps = laps[laps['Driver'] == driver]
            if piloto_laps.empty:
                return ('Desconhecido', 'N/A')

            equipe = piloto_laps.iloc[0]['Team']
            equipe = NOMES_EQUIPES_NORMALIZADOS.get(equipe, equipe)
            melhor_volta = melhores_voltas[melhores_voltas['Driver'] == driver]['LapTime'].iloc[0]
            volta_especifica = piloto_laps[piloto_laps['LapTime'] == melhor_volta]
            composto = None

            for col in ['Compound', 'TyreCompound', 'StintCompound']:
                if col in volta_especifica.columns:
                    composto = volta_especifica[col].iloc[0]
                    break

            return (equipe, composto if pd.notna(composto) else 'N/A')

        melhores_voltas[['Team', 'Compound']] = melhores_voltas['Driver'].apply(
            lambda d: pd.Series(pegar_info_piloto(d))
        )

        # 🔹 Adiciona cor
        melhores_voltas['Color'] = melhores_voltas['Team'].apply(
            lambda t: CORES_EQUIPES.get(t, '#FFFFFF')
        )

        # 🔹 Formatar tempo
        def formatar_tempo(td):
            total_seconds = td.total_seconds()
            minutos = int(total_seconds // 60)
            segundos = int(total_seconds % 60)
            milissegundos = int((total_seconds * 1000) % 1000)
            return f"{minutos}:{segundos:02d}.{milissegundos:03d}"

        melhores_voltas['LapTime'] = melhores_voltas['LapTime'].apply(formatar_tempo)

        # 🔹 Criar tabela
        tabela = html.Table(
            [
                html.Thead(html.Tr([
                    html.Th("Pos", style={'padding': '6px', 'border-bottom': '2px solid white'}),
                    html.Th("Equipe", style={'padding': '6px', 'border-bottom': '2px solid white'}),
                    html.Th("Piloto", style={'padding': '6px', 'border-bottom': '2px solid white'}),
                    html.Th("Pneu", style={'padding': '6px', 'border-bottom': '2px solid white'}),
                    html.Th("Melhor Volta", style={'padding': '6px', 'border-bottom': '2px solid white'})
                ])),
                html.Tbody([
                    html.Tr([
                        html.Td(idx + 1, style={'padding': '4px'}),
                        html.Td(html.Div(
                            style={
                                'width': '15px',
                                'height': '15px',
                                'backgroundColor': row['Color'],
                                'borderRadius': '50%',
                                'display': 'inline-block'
                            }
                        ), style={'padding': '4px'}),
                        html.Td(row['Driver'], style={'padding': '4px'}),
                        html.Td(row['Compound'], style={'padding': '4px'}),
                        html.Td(row['LapTime'], style={'padding': '4px'})
                    ], style={'color': 'white', 'border-bottom': '1px solid gray'})
                    for idx, row in melhores_voltas.iterrows()
                ])
            ],
            style={
                'width': '100%',
                'border-collapse': 'collapse',
                'margin-top': '10px',
                'background-color': '#111',
                'border-radius': '10px'
            }
        )

        return html.Div(
            tabela,
            style={'width': '100%', 'overflowY': 'auto', 'maxHeight': '70vh', 'padding': '10px'}
        )

    except Exception as e:
        return html.Div(f"❌ Erro ao gerar tabela: {str(e)}", style={'color': 'red', 'padding': '10px'})
