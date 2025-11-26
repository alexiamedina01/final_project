import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd


# main.py (al principio del archivo)
import sys
import os

# Añade la carpeta 'src' al sys.path para que Python encuentre el paquete final_project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # ruta del proyecto (donde está main.py)
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
from final_project.city import City

# Simulate
area_rates = {0: (100, 200), 1: (50, 250), 2: (250, 350), 3: (150, 450)}
HongKong = City(10, area_rates)
HongKong.initialize()  
for i in range(180):
    HongKong.iterate()


# Calculate
hosts = []
hosts_total_wealth = []
hosts_areas = []

for host in HongKong.hosts:
    total_wealth = host.profits
    for property_id in host.assets:
        final_price_property = HongKong.get_place(property_id).get_last_sale_price()
        total_wealth = total_wealth + final_price_property
    hosts.append(host.host_id)
    hosts_total_wealth.append(total_wealth)
    hosts_areas.append(host.area)

df = pd.DataFrame({
    'id': hosts, 
    'wealth': hosts_total_wealth, 
    'area':hosts_areas})

df = df.sort_values(by='wealth')

area_ids = list(area_rates.keys())
area_colors = ['red', 'blue', 'green', 'orange']
colors = [area_colors[area_id] for area_id in df['area']]

df.plot.bar(x='id', y='wealth', color=colors)
plt.xticks(fontsize=8)

# Create legend manually
patches = [mpatches.Patch(
                color=area_colors[i], 
                label=f'Area {area_ids[i]} (min: {area_rates[i][0]}, max: {area_rates[i][1]})'
            ) 
           for i in range(len(area_ids))]
plt.legend(handles=patches, title='Area')

# ---------------------------
# Guardar graph1 (en vez de plt.show())
# ---------------------------
os.makedirs("reports", exist_ok=True)
plt.savefig("reports/graph1.png", dpi=200)
plt.close()  # cerramos la figura actual
print("Saved reports/graph1.png")

# ---------------------------
# Código para generar graph2_v0.png y graph2_v1.png
# ---------------------------
import random
import numpy as np
import matplotlib.pyplot as plt

SEED = 12345
random.seed(SEED)
np.random.seed(SEED)

# helper: coeficiente de Gini
def gini(array):
    arr = np.array(array, dtype=float)
    if arr.size == 0:
        return 0.0
    if np.any(arr < 0):
        arr = arr - arr.min()
    arr += 1e-12
    arr = np.sort(arr)
    n = arr.size
    index = np.arange(1, n + 1)
    return (2.0 * np.sum(index * arr) / (n * np.sum(arr)) - (n + 1) / n)

# función que ejecuta la simulación y devuelve (assets_counts, host_areas)
def run_simulation_return_assets(area_rates, size=10, steps=180, city_class=City):
    # fijar semilla de nuevo para reproducibilidad
    random.seed(SEED)
    np.random.seed(SEED)
    c = city_class(size, area_rates)
    c.initialize()
    for _ in range(steps):
        c.iterate()
    assets_counts = [len(h.assets) for h in c.hosts]
    host_areas = [getattr(h, "area", None) for h in c.hosts]
    return assets_counts, host_areas

# versión modificada: permite que un mismo buyer haga múltiples compras por iteración
class CityAllowMultipleBuys(City):
    def approve_bids(self, bids):
        """Aprove bids but allow the same buyer to buy multiple properties in the same iteration.
           Sellers and property uniqueness are still enforced (a property sold once only)."""
        if not bids:
            return []
        import pandas as pd
        df = pd.DataFrame(bids).sort_values("spread", ascending=False)

        sold = set()
        approved = []

        for _, b in df.iterrows():
            pid = b["place_id"]
            if pid not in sold:
                approved.append(b)
                sold.add(pid)
        return approved

# helper plotting (assets per host, sorted, colored by area)
def plot_assets_distribution(assets_counts, host_areas, outpath, title):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)

    sorted_idx = np.argsort(assets_counts)
    sorted_assets = np.array(assets_counts)[sorted_idx]
    sorted_areas = np.array(host_areas)[sorted_idx]

    fig, ax = plt.subplots(figsize=(12,6))

    # coloreamos por área si está disponible
    area_colors = ['red', 'blue', 'green', 'orange']
    if None not in sorted_areas:
        colors = [area_colors[int(a) % len(area_colors)] for a in sorted_areas]
        ax.bar(range(len(sorted_assets)), sorted_assets, color=colors)
        # leyenda
        import matplotlib.patches as mpatches
        patches = [mpatches.Patch(color=area_colors[i], label=f"Area {i}") for i in range(len(area_colors))]
        ax.legend(handles=patches, title="Área origen", bbox_to_anchor=(1.02, 1), loc='upper left')
    else:
        ax.bar(range(len(sorted_assets)), sorted_assets)

    ax.set_xlabel("Hosts (ordenados por nº de propiedades)")
    ax.set_ylabel("Número de propiedades")
    ax.set_title(title)

    g = gini(assets_counts)
    ax.text(0.98, 0.95, f"Gini: {g:.3f}", transform=ax.transAxes, ha='right', va='top',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close(fig)
    print(f"Saved {outpath} (Gini: {g:.3f})")

# Ejecutar versión original (v0)
assets_v0, areas_v0 = run_simulation_return_assets(area_rates, size=10, steps=180, city_class=City)
plot_assets_distribution(
    assets_v0,
    areas_v0,
    outpath="reports/graph2_v0.png",
    title="Graph2 v0 — Distribución de propiedades por host (regla original)"
)

# Ejecutar versión modificada (v1)
assets_v1, areas_v1 = run_simulation_return_assets(area_rates, size=10, steps=180, city_class=CityAllowMultipleBuys)
plot_assets_distribution(
    assets_v1,
    areas_v1,
    outpath="reports/graph2_v1.png",
    title="Graph2 v1 — Distribución de propiedades por host (compradores pueden comprar varias propiedades/iteración)"
)




