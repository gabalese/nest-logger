import os
import sys

import elasticsearch
import csv
from dotenv import load_dotenv

load_dotenv(os.getenv('APP_CONFIG'))

ES_HOST = os.getenv('ES_HOST')
ES_USER = os.getenv('ES_USER')
ES_PASS = os.getenv('ES_PASS')
ES_INDEX_NAME = os.getenv('ES_INDEX_NAME')

if __name__ == '__main__':
    csv_file = sys.argv[1]

    es_client = elasticsearch.Elasticsearch(
        hosts=ES_HOST,
        http_auth=(ES_USER, ES_PASS),
        scheme="https",
        port=443
    )

    with open(csv_file) as f:
        csv_source = csv.reader(f, delimiter=',')
        for row in csv_source:
            es_client.index(
                index=ES_INDEX_NAME,
                doc_type='nest',
                body={
                    'timestamp': row[0],
                    'humidity_internal': row[1],
                    'humidity_external': row[2],
                    'temperature_external': row[3],
                    'temperature_internal_current': row[4],
                    'temperature_internal_target': row[5],
                    'status': row[6]
                }
            )
