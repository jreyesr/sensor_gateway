import argparse
import numpy as np
import pandas as pd
import seaborn as sns
from influxdb import DataFrameClient
import matplotlib.pyplot as plt

BORDER_PADDING = 0.001
STEP = 0.00001

parser = argparse.ArgumentParser()
parser.add_argument("metric", help="the metric to compute the map for")
parser.add_argument("--host", help="the IP or hostname of the InfluxDB server (port is fixed to 8086, dafault is localhost)", default="localhost")
parser.add_argument("-q", "--quiet", help="if set, don't show plots, only save image", action="store_true")
args = parser.parse_args()

QUIET = args.quiet

client = DataFrameClient(host=args.host, port=8086, database='sensors')
data = client.query('SELECT sensor_id, latitude as x, longitude as y, last("{}") as metric FROM weather GROUP BY sensor_id'.format(args.metric))
df = pd.concat(data.values()) # Join all rows of response in single table

df["metric"] = df["metric"].astype(float)
df["x"] = df["x"].astype(float)
df["y"] = df["y"].astype(float)

meas = df
extent = x_extent = x_min, x_max, y_min, y_max = [df.x.min()-BORDER_PADDING, df.x.max()+BORDER_PADDING,
                                                  df.y.min()-BORDER_PADDING, df.y.max()+BORDER_PADDING]
              
if not QUIET:                              
    fig, ax = plt.subplots(figsize=(10,6))
    ax.scatter(df.x, df.y, c=df.metric)
    ax.set_aspect(1)
    ax.set_xlim(*extent[:2])
    ax.set_ylim(*extent[2:])
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_title(args.metric)
    ax.grid(c='k', alpha=0.2)
    plt.show()

grid_x, grid_y = np.mgrid[x_min:x_max:STEP, y_min:y_max:STEP]

from scipy.interpolate import Rbf
# Make an n-dimensional interpolator
rbfi = Rbf(df.x, df.y, df.metric)
# Predict on the regular grid
di = rbfi(grid_x, grid_y)

mi = np.min(np.hstack([di.ravel(), df.metric.values]))
ma = np.max(np.hstack([di.ravel(), df.metric.values]))
if not QUIET:
    plt.figure(figsize=(15,15))
    c1 = plt.imshow(di.T, origin="lower", extent=extent, vmin=mi, vmax=ma)
    c2 = plt.scatter(df.x, df.y, s=60, c=df.metric, edgecolor='#ffffff66', vmin=mi, vmax=ma)
    plt.colorbar(c1, shrink=0.67)
    plt.show()

    por_hat = rbfi(df.x, df.y)
    sns.distplot(por_hat - df.metric)
    plt.show()

# Save the image to PNG, print the extent to console
plt.imsave("colormap.png", di, origin="lower", vmin=mi, vmax=ma)
print(x_min, x_max, sep=",")
print(y_min, y_max, sep=",")
