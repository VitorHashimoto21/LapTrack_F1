from flask import Flask, render_template
from dash import Dash
from modules.layout import criar_layout
from modules.callbacks import registrar_callbacks

# --- FLASK SERVER ---
server = Flask(__name__)

# --- ROTAS HTML ---
@server.route('/')
def home():
    return render_template('main.html')

@server.route('/sobre')
def sobre():
    return render_template('sobre.html')

@server.route('/contato')
def contato():
    return render_template('contato.html')

@server.route('/equipe')
def equipe():
    return render_template('equipe.html')

# --- DASH APP ---
app = Dash(
    __name__,
    server=server,
    url_base_pathname='/dash/',
    suppress_callback_exceptions=True
)

# Layout e callbacks
app.layout = criar_layout()
registrar_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
