from flask import Flask, request, jsonify

import requests

from utils import extract_domain_info, extract_subdomains, extract_asset_domains

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)
