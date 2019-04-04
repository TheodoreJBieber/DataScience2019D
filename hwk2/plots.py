import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import numpy as np
from basic_units import cm, inch

ufo_df = pd.read_csv("national_ufo_reports.csv")
ufo_df['date_time'] = pd.to_datetime(ufo_df['date_time'])
ufo_df['posted'] = pd.to_datetime(ufo_df['posted'])

# https://matplotlib.org/gallery/units/bar_unit_demo.html
N = 8
fig, ax = plt.subplots()
ind = np.arange(N)
width = 0.35

circles = ufo_df.loc[ufo_df.loc[:,'shape']=='Circle']
ccount = [t*cm for t in circles.groupby('month').size()]
p1 = ax.bar(ind, ccount, width, color='r', bottom=0*cm)

triangles = ufo_df.loc[ufo_df.loc[:,'shape']=='Triangle']
tcount = [t*cm for t in triangles.groupby('month').size()]
p2 = ax.bar(ind+width, tcount, width, color='y', bottom=0*cm)


difference = (ufo_df['posted'] - ufo_df['date_time'])

ax.set_title("Distribution of UFO reports by month")
plt.xlabel("Month")
plt.ylabel("# Reports")
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug'))

ax.legend((p1[0], p2[0]), ('Circle', 'Triangle'))
ax.yaxis.set_units(inch)
ax.autoscale_view()

plt.savefig("UFO_observations_by_month.png")
plt.clf()
plt.close()