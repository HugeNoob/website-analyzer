from bs4 import BeautifulSoup

from flask import Flask, request, jsonify

import requests


app = Flask(__name__)


@app.route('/')
def analyze_website():
    url = request.args.get('url')
    print("Parsed URL:", url)

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        html_content = response.text

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract information
        domains = extract_domains(soup)
        subdomains = extract_subdomains(soup)
        asset_domains = extract_asset_domains(soup)

        # Return the analysis results as JSON
        return jsonify({
            "info": domains,
            "subdomains": subdomains,
            "asset_domains": asset_domains
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch the website data."})


def extract_domains(soup):
    return


def extract_subdomains(soup):
    return


def extract_asset_domains(soup):
    return


if __name__ == '__main__':
    app.run(debug=True)

