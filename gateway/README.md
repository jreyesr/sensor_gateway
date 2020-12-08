# InfluxDB sensor gateway

A gateway program that sits near a sensor network and exposes a HTTP server which collects the sensor readings to InfluxDB.

It uses Python and the InfluxDB client library to send INSERT requests to the DB. There is no provision for reading data back or displaying it - it's assumed that a third party application (such as [Grafana](https://grafana.com/oss/grafana/)) will be used to visualize the ingested data.

## Installation

1. InfluxDB must be already installed and running in the local computer.
1. Clone this repo.
1. Install the requirements with `pip install -r requirements.txt`.
1. Run `python main.py` in a Bash session.

## Configuration

The InfluxDB database must already exist. The following parameters can be configured:
* Auth information: DB_USERNAME and DB_PASSWORD. These are required to authenticate to InfluxDB. A default installation of InfluxDB can leave these empty.
* Database name: Set to `sensors` by default.
* Measurement (AKA table) name: Where is the data written. There is currently a single measurement, since all sensors are expected to be of the same type and therefore provide the same data types. Edit the variable MEASUREMENT_NAME, located at the top of the Python script, to change it.
* Sensor locations: the sensors will be identified by an ID, and the dictionary SENSOR_LOCATIONS will provide a mapping to a latitude and longitude, which will be used to present the data in a map. There must be an entry for each sensor that will connect to the gateway. Nonexistent sensors will be rejected with a 404 error code.

## API

The application exposes a very simple API (as in, just a single-endpoint) to submit sensor data. All data must be submitted as JSON strings in the body of the request.

* POST `/upload`: Uploads a single sensor reading. Parameters:
    * `sensor_id`: The unique ID of the sensor. Will be internally translated to a (latitude, longitude) tuple using the SENSOR_LOCATIONS dictionary.
    * (optional) `time`: Overrides the automatic timestamping of InfluxDB. If not present, InfluxDB will timestamp the data with the current date and time. Must be provided in RFC3339 format (for example, `2020-11-10T23:01:02-02:00`). 
    * (any extra fields) Will be passed directly to InfluxDB as measurement fields. Don't provide units with the data! (i.e., if measuring 25º C, just send `25`). That allows ordering and parsing. Units should be set on the visualizer (for example, Grafana has a setting to show units on panels).

## Additional functionality

### Map interpolation
TODO Add docs for calling the interpolation script

### Serving interpolated map

Any files placed on the `static/` folder will be automagically served on `http://<ip>:5000/static/filename.extension`. No further configuration is required. This can be used to display the interpolated maps (generated on the previous section) to a frontend.