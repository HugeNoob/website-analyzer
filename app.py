from collections import defaultdict

from flask import Flask, request, jsonify

from flask_sock import Sock

from json import loads, dumps

import requests

from utils import extract_domain_info, extract_subdomains, extract_asset_domains

app = Flask(__name__)
sock = Sock(app)


@app.route('/')
def analyze_website():
    url = request.args.get('url')

    try:
        # Extract information
        domain_info = extract_domain_info(url)
        subdomains = extract_subdomains(url)
        asset_domains = extract_asset_domains(url)

        # Return the analysis results as JSON
        return jsonify({
            "info": domain_info,
            "subdomains": subdomains,
            "asset_domains": asset_domains
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch the website data."})


@sock.route('/ws')
def echo(ws):
    analyzed_information = defaultdict(
        lambda: "Information has not been initialised.")

    while True:
        data_string = ws.receive()

        if data_string:
            data = loads(data_string)

            if "url" in data:
                recv_url = data["url"]
                if not recv_url.startswith("https://") or recv_url.startswith("http://"):
                    url = "https://" + recv_url
                else:
                    url = recv_url

                analyzed_information = {
                    "info": extract_domain_info(url),
                    "subdomains": extract_subdomains(url),
                    "asset_domains": extract_asset_domains(url)
                }

                resp = {"data": f'session created for {recv_url}'}
                ws.send(dumps(resp))

            elif "operation" in data:
                op = data["operation"]

                if op == "get_info":
                    info = analyzed_information["info"]
                elif op == "get_subdomains":
                    info = analyzed_information["subdomains"]
                elif op == "get_asset_domains":
                    info = analyzed_information["asset_domains"]
                elif op == "close":
                    ws.close(message="Websocket closed.")
                else:
                    info = "Could not interpret your query."

                resp = {"data": info}
                ws.send(dumps(resp))
            else:
                resp = {"data": "Could not interpret your query."}
                ws.send(dumps(resp))


if __name__ == '__main__':
    app.run(debug=True)
