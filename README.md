# LapTrack F1 - Dashboard de Telemetria

<img src="https://docs.fastf1.dev/_static/logo.png" alt="Logo" width="200"/> <img src ="https://www.pngmart.com/files/10/Formula-1-Logo-PNG-File.png" alt ="Logof1" width="200"/>
 <!-- opcional, caso queira colocar uma imagem de topo -->

## Descrição

O **LapTrack F1** é um dashboard interativo desenvolvido em **Dash** e **Plotly**, que permite visualizar telemetria, tempos de volta, posições e desempenho de pilotos em corridas de Fórmula 1. Ele utiliza a biblioteca [FastF1](https://theoehrly.github.io/Fast-F1/) para coletar dados de corrida em tempo real.

O projeto é voltado para análise de desempenho de pilotos e equipes, fornecendo gráficos, mapas de pista e tabelas de classificação de forma interativa.

## Funcionalidades

- Visualização de tempos de volta por piloto
- Comparação de desempenho entre pilotos
- Mapas de circuito com posições e setores
- Tabelas de classificação e estatísticas de corrida
- Personalização de cores por equipe
- Layout responsivo e moderno

## Estrutura do Projeto
`````
LapTrack_2.0/
|
├─ app.py                # Arquivo a ser executado para rodar a Dash
├─ README.md             # Descrição do projeto
├─ requirements.txt      # Bibliotecas e versões usadas
├─ cache                 # Crie um cache para armazenar os dados do fastf1
├─ .gitignore            # Arquivos a serem ignorados pelo Git
|
├─ modules/              # Módulos Python
| ├─ init.py
| ├─ callbacks.py        # Callbacks do Dash
| ├─ layout.py           # Layout do Dash
| ├─ tabela_pilotos.py   # Função para gerar a tabela de pilotos
| ├─ track_map.py        # Função para gerar o mapa do circuito
| └─ utils.py            # Cores das equipes
`````
