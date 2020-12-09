from influxdb import InfluxDBClient
from flask import Flask, request, abort
import subprocess
import shutil

DB_NAME = "sensors"
DB_USERNAME = ""
DB_PASSWORD = ""
MEASUREMENT_NAME = "weather"
SENSOR_LOCATIONS = {
    "CAF003": [ -117.086665608667218, 46.778784151233317 ], # "sensor_id": (lng, lat),
    "CAF007": [ -117.084988619820408, 46.778623424801346 ],
    "CAF009": [ -117.084150325409311, 46.778669039811675 ],
    "CAF019": [ -117.088447197328591, 46.778818784717203 ],
    "CAF031": [ -117.083456596480502, 46.779020513199683 ],
    "CAF033": [ -117.082618198242201, 46.779003123270108 ],
    "CAF035": [ -117.081779582529762, 46.778841741546273 ],
    "CAF061": [ -117.080797577763022, 46.779148408867975 ],
    "CAF067": [ -117.078269529392202, 46.779267154149501 ],
    "CAF075": [ -117.085278370520783, 46.779613111667338 ],
    "CAF079": [ -117.083614668650597, 46.779587341904936 ],
    "CAF095": [ -117.088055665014153, 46.779709998770109 ],
    "CAF119": [ -117.077995217419087, 46.779807288137121 ],
    "CAF125": [ -117.086432107653025, 46.780215186643751 ],
    "CAF129": [ -117.084755075059334, 46.780054456859411 ],
    "CAF133": [ -117.083091442900439, 46.780082674107753 ],
    "CAF135": [ -117.082253220155906, 46.780191268934331 ],
    "CAF139": [ -117.080563033756178, 46.77998549162168 ],
    "CAF141": [ -117.079738093216463, 46.78022004623314 ],
    "CAF163": [ -117.081231772041122, 46.78041697625283 ],
    "CAF173": [ -117.077052716934517, 46.780284879451074 ],
    "CAF197": [ -117.077695062708415, 46.780599414055892 ],
    "CAF201": [ -117.086236903373546, 46.781025253829711 ],
    "CAF205": [ -117.084560057544309, 46.780999507715627 ],
    "CAF209": [ -117.0828832685213, 46.781009733431659 ],
    "CAF215": [ -117.080420611152206, 46.781110480588261 ],
    "CAF217": [ -117.079542801759331, 46.781039101163202 ],
    "CAF231": [ -117.083800619314815, 46.781234043152466 ],
    "CAF237": [ -117.081219930719712, 46.78125390188309 ],
    "CAF245": [ -117.077918722201758, 46.781265196125219 ],
    "CAF275": [ -117.084338720299371, 46.781872584614099 ],
    "CAF308": [ -117.080959224055093, 46.782118001026653 ],
    "CAF310": [ -117.08008170448943, 46.782253605022042 ],
    "CAF312": [ -117.07928251845405, 46.782209165895921 ],
    "CAF314": [ -117.078417766861421, 46.782119770592587 ],
    "CAF316": [ -117.077579270379246, 46.782066347392274 ],
    "CAF349": [ -117.084182836061288, 46.782718615504052 ],
    "CAF351": [ -117.083331321409844, 46.782728237772908 ],
    "CAF357": [ -117.080842197005225, 46.782703025735145 ],
    "CAF377": [ -117.081641500451298, 46.782819446738628 ],
    "CAF397": [ -117.082650966108687, 46.783295674834676 ],
    "CAF401": [ -117.080974064917442, 46.783278875332414 ]
}

client = InfluxDBClient('localhost', 8086, DB_USERNAME, DB_PASSWORD, DB_NAME)
app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_sensor_meas():
    data = request.json

    # ensure sensor is on location map
    if data.get("sensor_id") not in SENSOR_LOCATIONS:
        abort(404)
    
    lng, lat = SENSOR_LOCATIONS[data["sensor_id"]] # lng, lat are reversed in SENSOR_LOCATIONS!
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
        
@app.route('/recompute', methods=['POST'])
def recompute_map():
    data = request.json
    metric = data.get("metric", "temp")
    
    ans = subprocess.check_output(["python3",  "../genmap_influx.py", "localhost", "quiet"])
    shutil.move("colormap.png", "static/colormap.png")

    return ""

if __name__ == "__main__":
    app.run(debug=False)
