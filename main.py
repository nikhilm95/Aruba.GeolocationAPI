#!/usr/bin/env python
# encoding: utf-8
import json
import requests
import os
import redis
from dotenv import load_dotenv
from flask import Flask, request, jsonify

app = Flask(__name__)


load_dotenv()
cache = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"))


@app.route("/", methods=["POST"])
def update_record():
    payload = json.loads(request.data)
    if not "apscan_data" in payload:
        return None, 400
    records = payload["apscan_data"]
    new_record = []
    for r in records:
        bssid = r["bssid"] if "bssid" in r else None
        if bssid is None:
            new_record.append({})
        else:
            cache_data = cache.get(bssid)
            if cache_data is None:
                query = {"macAdress": bssid}
                response = requests.post(
                    f"https://www.googleapis.com/geolocation/v1/geolocate?key={os.getenv('GOOGLE_API_KEY')}",
                    json=query
                )
                if response.status_code == 200:
                    data = response.json()
                    cache.set(bssid, response.text)
                    new_record.append(data)
                else:
                    new_record.append({})
            else:
                new_record.append(json.loads(cache_data))
    return jsonify({"results": new_record})


app.run(host="0.0.0.0", debug=os.environ.get("DEBUG", True))
