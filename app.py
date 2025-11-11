from flask import Flask, render_template
from dash import Dash
from modules.layout import criar_layout
from modules.callbacks import registrar_callbacks

# --- FLASK SERVER ---
server = Flask(__name__)

# Página inicial HTML (a tela estilizada)
@server.route('/')
def home():
    return render_template('main.html')

# --- DASH APP ---
app = Dash(
    __name__,
    server=server,
    url_base_pathname='/dash/',   # necessário terminar com '/'
    suppress_callback_exceptions=True,
    title="LapTrack F1"
)

# Layout e callbacks do seu projeto
app.layout = criar_layout()
registrar_callbacks(app)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)
