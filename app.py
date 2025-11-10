from dash import Dash
from modules.layout import criar_layout
from modules.callbacks import registrar_callbacks
from dash import dcc, html, Input, Output
from modules.track_map import gerar_mapa_comparativo
from modules.tabela_pilotos import gerar_tabela_pilotos_sessao
import modules.utils 


import fastf1

# Ativar cache
fastf1.Cache.enable_cache('cache') 

# Inicializar app
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Layout
app.layout = criar_layout()

# Callbacks
registrar_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
