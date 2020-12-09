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
Call the script as `python genmap_influx.py localhost noquiet`. The first argument is the IP or hostname of the InfluxDB server (expected to be localhost). The second argument must be either `quiet` or `noquiet`. A value of `quiet` supresses the Matplotlib graphs and therefore allows the script to run without user interaction. `noquiet` is used when running the script directly from console.

The database must have a `sensors` database which must contain a `weather` table, which must in turn contain measurements with tags `sensor_id`, `latitude` and `longitude`, and value `temp`.

TODO: Change code to allow the specific column (currently hardcoded to `temp`) to be specified in the command line.

### Results
The script creates a PNG image in false color. The coordinates of the limits of the PNG image (in the form `min_lng, min_lat, max_lng, max_lat`) are printed to standard output. 

The image is expected to be served by a web server and used, for example, in [the updated WorldMap panel for Grafana](https://github.com/panodata/grafana-map-panel) (see [here](https://github.com/panodata/grafana-map-panel#image-overlay) for instructions).
