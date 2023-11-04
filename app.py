from bs4 import BeautifulSoup

from collections import defaultdict

from dotenv import load_dotenv

from flask import Flask, request, jsonify

from urllib.parse import urlparse

import requests

from os import getenv

from socket import gethostbyname, gaierror

app = Flask(__name__)

load_dotenv()


@app.route('/')
def analyze_website():
    url = request.args.get('url')

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        html_content = response.text

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract information
        domain_info = extract_domain_info(url)
        subdomains = extract_subdomains(url)
        asset_domains = extract_asset_domains(soup)

        # Return the analysis results as JSON
        return jsonify({
            "info": domain_info,
            "subdomains": subdomains,
            "asset_domains": asset_domains
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch the website data."})


def extract_domain_info(url):
    domain = urlparse(url).netloc

    try:
        ip = gethostbyname(domain)
    except gaierror:
        ip = None
        print("Failed to get IP address.")

    if ip:
        location_data = get_ip_location_data(ip)
    else:
        location_data = defaultdict(lambda: "Failed to get location data")

    return {
        "ip": ip,
        "isp": location_data["isp"],
        "organization": location_data["organization"],
        "asn": location_data["asn"],
        "location": location_data["location"],
    }


def get_ip_location_data(ip):
    IP_API_KEY = getenv("IP_API_KEY")
    response = requests.get(
        f'https://api.ipgeolocation.io/ipgeo?apiKey={IP_API_KEY}&ip={ip}').json()

    # The API above does not provide asn in response, despite mentioning it in documentation
    # Hence, a different endpoint is needed for asn specifically
    asn = requests.get(f'https://ipapi.co/{ip}/json/').json().get("asn")

    location_data = {
        "isp": response.get("isp"),
        "organization": response.get("organization"),
        "asn": asn,
        "location": response.get("country_code2"),
    }
    return location_data


def extract_subdomains(url):
    parts = urlparse(url).netloc.split('.')
    domain = '.'.join(parts[-2:])

    SUBDOMAIN_API_KEY = getenv("SUBDOMAIN_API_KEY")
    response = requests.get(
        f'https://subdomains.whoisxmlapi.com/api/v1?apiKey={SUBDOMAIN_API_KEY}&domainName={domain}').json()

    subdomains = []
    for record in response.get("result").get("records"):
        subdomains.append(record["domain"])

    return subdomains


def extract_asset_domains(soup):
    return


if __name__ == '__main__':
    app.run(debug=True)

