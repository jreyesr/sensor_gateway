from influxdb import InfluxDBClient
from flask import Flask, request, abort

DB_NAME = "sensors"
DB_USERNAME = ""
DB_PASSWORD = ""
MEASUREMENT_NAME = "weather"
SENSOR_LOCATIONS = { # "sensor_id": (lat, lng),
    "SEN001": (10, 12),
    "SEN002": (12, 16),
    "SEN003": (21, 17),
}

client = InfluxDBClient('localhost', 8086, DB_USERNAME, DB_PASSWORD, DB_NAME)
app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def hello_world():
    data = request.json

    # ensure sensor is on location map
    if data.get("sensor_id") not in SENSOR_LOCATIONS:
        abort(404)
    
    lat, lng = SENSOR_LOCATIONS[data["sensor_id"]]
    db_data = {
        "measurement": MEASUREMENT_NAME,
        "tags": {
            "sensor_id": data["sensor_id"],
            "latitude": lat,
            "longitude": lng,
        },
        # "time": "2009-11-10T23:00:00Z", # will be added later if required
        "fields": { k: v 
            for k, v in data.items() 
            if k not in ("sensor_id", "time")
        } # every other dict entry goes here!
    }
    if "time" in data: # add time to data if specified by user
        db_data["time"] = data["time"]
    
    ret = client.write_points([db_data]) # write_points takes a LIST of dicts!
    
    if ret:
        return ""
    else:
        abort(404) # write failed

if __name__ == "__main__":
    app.run(debug=False)