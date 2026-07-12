from flask import Flask, render_template, jsonify, request
import requests


app = Flask(__name__)


API_URL = {
    # asteroidi vicino alla Terra
    "asteroidi_near_terra":     "https://api.nasa.gov/neo/rest/v1/feed?api_key=DEMO_KEY",
    # lista di tutti dataset del comune di milano
    "dataset_com_milano":       "https://dati.comune.milano.it/api/3/action/package_list",
    # lista di tutti dataset del comune di firenze
    "dataset_com_firenze":      "https://data.comune.fi.it/datastore/api/package_list",
    # lista di tutti dataset del comune di verona
    "dataset_com_verona":       "https://dati.comune.verona.it/api/3/action/package_list",
    # eventi sismici avvenuti in un range di date
    "eventi_sismici":           "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-12-01&endtime=2025-12-31",
    # dati meteo verona
    "meteo_verona":             "https://api.open-meteo.com/v1/forecast?latitude=45.4384&longitude=10.9916&hourly=temperature_2m"
}


@app.route("/data/")
def data():
    name = request.args.get("url")

    if name not in API_URL:
        return jsonify({"status": "error", "code": 404}), 404

    r = requests.get(API_URL[name], timeout=5)
    r.raise_for_status()
    return jsonify(r.json())


@app.route("/")
def homepage():
    return render_template("index.html", urls=API_URL)


if __name__ == "__main__":
    app.run(debug=True)
