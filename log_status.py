import datetime

import nest
import forecastio
from collections import namedtuple
from dotenv import load_dotenv
import os
load_dotenv(os.getenv('APP_CONFIG'))


NEST_CLIENT_ID = os.getenv('NEST_CLIENT_ID')
NEST_CLIENT_SECRET = os.getenv('NEST_CLIENT_SECRET')
NEST_CLIENT_TOKEN = os.getenv('NEST_CLIENT_TOKEN')
DARK_SKY_API_KEY = os.getenv('DARK_SKY_API_KEY')
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')

Measurement = namedtuple(
    'Measurement',
    'timestamp humidity_internal humidity_external temperature_internal_current temperature_internal_target temperature_external status'
)

if __name__ == '__main__':
    nest_client = nest.Nest(client_id=NEST_CLIENT_ID, client_secret=NEST_CLIENT_SECRET)
    nest_client._session.auth._access_token = NEST_CLIENT_TOKEN
    thermostat = nest_client.thermostats[0]

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
