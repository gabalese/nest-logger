import datetime
import os
from collections import namedtuple

import elasticsearch
import forecastio
import nest

NEST_CLIENT_ID = os.getenv('NEST_CLIENT_ID')
NEST_CLIENT_SECRET = os.getenv('NEST_CLIENT_SECRET')
NEST_CLIENT_TOKEN = os.getenv('NEST_CLIENT_TOKEN')
DARK_SKY_API_KEY = os.getenv('DARK_SKY_API_KEY')
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')
ES_HOST = os.getenv('ES_HOST')
ES_USER = os.getenv('ES_USER')
ES_PASS = os.getenv('ES_PASS')
ES_INDEX_NAME = os.getenv('ES_INDEX_NAME')

Measurement = namedtuple(
    'Measurement',
    'timestamp humidity_internal humidity_external temperature_internal_current temperature_internal_target temperature_external status'
)

if __name__ == '__main__':
    nest_client = nest.Nest(client_id=NEST_CLIENT_ID, client_secret=NEST_CLIENT_SECRET)
    nest_client._session.auth._access_token = NEST_CLIENT_TOKEN
    thermostat = nest_client.thermostats[0]
    es_client = elasticsearch.Elasticsearch(
        hosts=ES_HOST,
        http_auth=(ES_USER, ES_PASS),
        scheme="https",
        port=443
    )

    forecast = forecastio.load_forecast(DARK_SKY_API_KEY, LATITUDE, LONGITUDE)
    current = forecast.currently()

    measurement = Measurement(
        timestamp=datetime.datetime.now(),
        humidity_internal=thermostat.humidity, humidity_external=current.d['humidity'] * 100,
        temperature_internal_current=thermostat.temperature, temperature_internal_target=thermostat.target,
        temperature_external=current.d['temperature'], status=thermostat.hvac_state

    )

    print(
        measurement.timestamp.isoformat(),
        measurement.humidity_internal,
        measurement.humidity_external,
        measurement.temperature_external,
        measurement.temperature_internal_current,
        measurement.temperature_internal_target,
        measurement.status
    )

    es_client.index(
        index=ES_INDEX_NAME,
        doc_type='nest',
        body={
            'timestamp': measurement.timestamp.isoformat(),
            'humidity_internal': measurement.humidity_internal,
            'humidity_external': measurement.humidity_external,
            'temperature_external': measurement.temperature_external,
            'temperature_internal_current': measurement.temperature_internal_current,
            'temperature_internal_target': measurement.temperature_internal_target,
            'status': measurement.status
        }
    )
