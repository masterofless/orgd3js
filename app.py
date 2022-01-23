from flask import Flask
from flask import make_response

import requests
import csv
from io import StringIO
import json

from logging.config import dictConfig

# leave this in if you ever want to see your precious logs again
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})
app = Flask(__name__)

DATA_URL = 'https://www.nasa.gov/digitalstrategy/bureaudirectory.json'

@app.route('/data')
def data():
    app.logger.info(f'downloading from {DATA_URL}')
    download = requests.get(DATA_URL)
    content = json.loads(download.content.decode('utf-8'))

    headers = ['name', 'imageUrl', 'area', 'profileUrl', 'office', 'tags', 'isLoggedUser', 'positionName', 'id', 'parentId', 'size']
    csvResult = StringIO('')
    writer = csv.writer(csvResult)
    for row in content['leaders']:
        person = [f"{row['firstName']} {row['lastName']}"]
        app.logger.debug(f'person: {person}')
        writer.writerow(person)
    output = make_response(csvResult.getvalue())
    output.headers["Content-type"] = "text/csv"
    output.headers["Content-Disposition"] = "attachment; filename=people.csv"
    return output

@app.route('/')
def index():
    return 'This is your index'

app.run(host='0.0.0.0', port=8080)
