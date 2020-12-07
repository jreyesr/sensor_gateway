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
TODO requirements, installation, usage, results
