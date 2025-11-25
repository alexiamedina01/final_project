import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
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

plt.show()
