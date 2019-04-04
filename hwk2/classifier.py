from sklearn.datasets import load_iris
from sklearn import tree
import numpy as np

ufo_df = pd.read_csv("national_ufo_reports.csv")
ufo_df['date_time'] = pd.to_datetime(ufo_df['date_time'])
ufo_df['posted'] = pd.to_datetime(ufo_df['posted'])

