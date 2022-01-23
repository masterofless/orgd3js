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

    headers = ['name', 'imageUrl', 'area', 'profileUrl', 'office', 'tags', 'isLoggedUser', 'positionName', 'id', 'parentId', 'size']
    csvResult = StringIO('')
    writer = csv.writer(csvResult)
    writer.writerow(headers)

    app.logger.info(f'downloading from {DATA_URL}')
    download = requests.get(DATA_URL)
    content = json.loads(download.content.decode('utf-8'))

    for row in content['leaders']:
        person = [
            f"{row['firstName']} {row['lastName']}", # name
            f"", # imageurl
            f"{row['employmentType']}", # area
            f"", # profileurl
            f"", # office
            f"", # tags
            f"", # isLoggedUser
            f"{row['evaluationRatingOfficialTitle']}", # positionName
            f"", # id
            f"", # parentId
            f"", # size
        ]
        writer.writerow(person)

    output = make_response(csvResult.getvalue())
    output.headers["Content-type"] = "text/csv"
    output.headers["Content-Disposition"] = "attachment; filename=people.csv"
    return output

@app.route('/')
def index():
    return 'This is your index'

app.run(host='0.0.0.0', port=8080)
