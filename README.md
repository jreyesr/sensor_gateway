# Weather sensor interpolation & gateway

This repo contains code to receive data from weather sensors in a sensor network and bridge them to an InfluxDB database (see [gateway](gateway), and create an interpolated heatmap from the measurements, to be displayed in a map (see [genmap](genmap_influx.py)).

## Requirements

* Python and the requirements in [requirements.txt](requirements.txt)
* An InfluxDB database running on port 8086 of localhost.
* A Grafana instance that can talk to the InfluxDB database, preferably on localhost to avoid CORS issues.
* (Optional?) A reverse proxy to serve both port 5000 (the gateway, Python + Flask) and port 3000 (Grafana) on the same IP/domain.

## Sensor network gateway

See [the gateway readme](gateway/README.md) for more information.

## Interpolated map

The [genmap_influx.py](genmap_influx.py) script generates an interpolated map from the latest measurements in the InfluxDB database.
The resulting PNG can be used as an overlay to a map.

### Requirements
The `genmap_influx.py` script uses the requirements on [requirements.txt](requirements.txt).

### Installation
No installation is required. The `genmap_influx.py` script is expected to be invoked from the Flask server, but it can also be invoked manually.

### Usage

Usage information is available by running `python genmap.py --help`, which outputs the following:

```
usage: genmap_influx.py [-h] [--host HOST] [-q] metric

positional arguments:
  metric       the metric to compute the map for

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  the IP or hostname of the InfluxDB server (port is fixed to
               8086, dafault is localhost)
  -q, --quiet  if set, don't show plots, only save image
```

Call the script as `python genmap_influx.py <metric>`. 

The database must have a `sensors` database which must contain a `weather` table, which must in turn contain measurements with tags `sensor_id`, `latitude` and `longitude`, and a value column with the same name as the provided `metric`.

There are optional arguments: to specify the IP or hostname of the InfluxDB server (default is localhost) and to run the script without user interaction (i.e. supressing the Matplotlib graphs and saving the map directly to disk, without opening windows). This last option is expected to be used when calling the script from the gateway server.

### Results
The script creates a PNG image in false color. The coordinates of the limits of the PNG image (in the form `min_lat, max_lat` and `min_lng, max_lng`) are printed to standard output.  The last two lines of the standard output, therefore, can be used to configure the bounds of the image when displayed in a map.

The image is expected to be served by a web server and used, for example, in [the updated WorldMap panel for Grafana](https://github.com/panodata/grafana-map-panel) (see [here](https://github.com/panodata/grafana-map-panel#image-overlay) for instructions). 
