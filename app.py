#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from google.cloud import bigquery

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "employee.age":
        return {}
client = bigquery.Client()
    # [END create_client]
    # [START run_query]
    query_results = client.run_sync_query("""
        SELECT
            APPROX_TOP_COUNT(corpus, 10) as title
        FROM `publicdata.samples.shakespeare`;""")

    # Use standard SQL syntax for queries.
    # See: https://cloud.google.com/bigquery/sql-reference/
    query_results.use_legacy_sql = False

    query_results.run()
    # [END run_query]

    # [START print_results]
    # Drain the query results by requesting a page at a time.
    page_token = None

    while True:
        rows, total_rows, page_token = query_results.fetch_data(
            max_results=10,
            page_token=page_token)

        for row in rows:
            print("Response:")
            print(total_rows)
    
        if not page_token:
            break
    # [END print_results]


if __name__ == '__main__':
    query_shakespeare()


    return {
        "speech": total_rows,
        "displayText": total_rows,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-miibottest"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
