from dash import Dash
<<<<<<< HEAD:modules/app.py
from layout import criar_layout
from callbacks import registrar_callbacks
=======
from modules.layout import criar_layout
from modules.callbacks import registrar_callbacks
>>>>>>> 91643d7cc5c425dd698398e000c926d0d1649ddd:app.py
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
