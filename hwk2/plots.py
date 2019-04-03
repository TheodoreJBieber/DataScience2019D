import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl

ufo_df = pd.read_csv("national_ufo_reports.csv")
ufo_df['date_time'] = pd.to_datetime(ufo_df['date_time'])

plt.xlabel("Month of report")
plt.ylabel("Number of reports")
plt.title("Distribution of UFO reports by month")
plt.grid(b=None)

# div = 25
# tics = [i*div for i in range(1,8)]
# plt.xticks(ticks=tics,labels=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"])

ufo_df['month'].hist(bins=12)

plt.savefig("UFO_observations_by_month.png")