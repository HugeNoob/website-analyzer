from analyzer import extract_domain_info, extract_subdomains, extract_asset_domains

from collections import defaultdict

from flask import Flask, request, jsonify

from flask_sock import Sock

from json import loads, dumps

from websocket import process_message

app = Flask(__name__)
sock = Sock(app)


@app.route('/')
def analyze_website():
    url = request.args.get('url')

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


@sock.route('/ws')
def echo(ws):
    analyzed_information = defaultdict(
        lambda: "Information has not been initialised.")

    while True:
        msg_string = ws.receive()

        if msg_string:
            msg = loads(msg_string)
            resp = process_message(msg, analyzed_information)
            ws.send(dumps(resp))


if __name__ == '__main__':
    app.run(debug=True)
