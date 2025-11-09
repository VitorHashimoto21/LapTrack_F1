import fastf1
import matplotlib
matplotlib.use('Agg')  
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap
import numpy as np
import io
import base64
import pandas as pd
from utils import cores_equipes

def gerar_mapa_comparativo(corrida, ano, piloto1, piloto2, sessao):
    try:
        
        cor_piloto1 = cores_equipes.get(piloto1, '#FFFFFF')
        cor_piloto2 = cores_equipes.get(piloto2, '#AAAAAA')

        # Carregar sessão
        session_event = fastf1.get_session(ano, corrida, sessao)
        session_event.load()

        # Voltas mais rápidas
        lap1 = session_event.laps.pick_driver(piloto1).pick_fastest()
        lap2 = session_event.laps.pick_driver(piloto2).pick_fastest()

        # Telemetria
        tel1 = lap1.get_telemetry().add_distance()
        tel2 = lap2.get_telemetry().add_distance()

        tel1['Driver'] = piloto1
        tel2['Driver'] = piloto2
        telemetry_drivers = pd.concat([tel1, tel2])

        # Dividir em minisectores
        num_minisectors = 21
        total_distance = telemetry_drivers['Distance'].max()
        minisector_length = total_distance / num_minisectors

        telemetry_drivers['Minisector'] = telemetry_drivers['Distance'].apply(
            lambda dist: int((dist // minisector_length) + 1)
        )

        avg_speed = telemetry_drivers.groupby(['Minisector', 'Driver'])['Speed'].mean().reset_index()
        fastest_driver = avg_speed.loc[avg_speed.groupby('Minisector')['Speed'].idxmax()]
        fastest_driver = fastest_driver[['Minisector', 'Driver']].rename(columns={'Driver': 'Fastest_driver'})

        telemetry_drivers = telemetry_drivers.merge(fastest_driver, on='Minisector')
        telemetry_drivers = telemetry_drivers.sort_values(by='Distance')

        telemetry_drivers.loc[telemetry_drivers['Fastest_driver'] == piloto1, 'Fastest_driver_int'] = 1
        telemetry_drivers.loc[telemetry_drivers['Fastest_driver'] == piloto2, 'Fastest_driver_int'] = 2

        # Plot
        x = np.array(telemetry_drivers['X'].values)
        y = np.array(telemetry_drivers['Y'].values)

        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        cmap = ListedColormap([cor_piloto1, cor_piloto2])

        lc_comp = LineCollection(segments, cmap=cmap, norm=plt.Normalize(1, 3))
        lc_comp.set_array(telemetry_drivers['Fastest_driver_int'].to_numpy().astype(float))
        lc_comp.set_linewidth(4)

        plt.rcParams['figure.figsize'] = [14, 8]
        fig, ax = plt.subplots()
        ax.add_collection(lc_comp)
        ax.axis('equal')
        ax.axis('off')
        ax.set_facecolor('#0c0c0c')
        fig.patch.set_facecolor('#0c0c0c')

        plt.title(f"{ano} — {piloto1} vs {piloto2} ({sessao})",
                  color='white', fontsize=12)

        # Barra de cor
        cbar = plt.colorbar(mappable=lc_comp, ax=ax, boundaries=np.arange(1, 4))
        cbar.set_ticks(np.arange(1.5, 3.5))
        cbar.set_ticklabels([piloto1, piloto2])
        cbar.set_label('Piloto mais rápido', color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight', pad_inches=0.1, facecolor='#0c0c0c')
        plt.close(fig)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return f"data:image/png;base64,{img_base64}"

    except Exception as e:
        print(f"Erro ao gerar mapa: {e}")
        return None
