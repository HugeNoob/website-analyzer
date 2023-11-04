from collections import defaultdict

from cymruwhois import Client

from bs4 import BeautifulSoup

from dotenv import load_dotenv

from os import getenv

import requests

from re import match

from socket import gethostbyname, gaierror

from utils import get_domain_from_url

load_dotenv()


def extract_domain_info(url):
    domain = get_domain_from_url(url)

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
    # Hence, a different library is used for asn specifically
    asn = "AS" + Client().lookup(ip).asn

    location_data = {
        "isp": response.get("isp"),
        "organization": response.get("organization"),
        "asn": asn,
        "location": response.get("country_code2"),
    }
    return location_data


def extract_subdomains(url):
    domain = get_domain_from_url(url, keep_www=False)

    SUBDOMAIN_API_KEY = getenv("SUBDOMAIN_API_KEY")
    response = requests.get(
        f'https://subdomains.whoisxmlapi.com/api/v1?apiKey={SUBDOMAIN_API_KEY}&domainName={domain}').json()

    subdomains = []
    for record in response["result"]["records"]:
        subdomains.append(record["domain"])

    return subdomains


def extract_asset_domains(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP request errors
    html_content = response.text

    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    javascripts = set()
    for script in soup.find_all('script', src=True):
        src = script['src']
        if src and match(r'^https?://', src):
            javascripts.add(get_domain_from_url(src))

    stylesheets = set()
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href')
        if href and match(r'^https?://', href):
            stylesheets.add(get_domain_from_url(href))

    images = set()
    for img in soup.find_all('img', src=True):
        src = img['src']
        if src and match(r'^https?://', src):
            images.add(get_domain_from_url(src))

    iframes = set()
    for iframe in soup.find_all('iframe', src=True):
        src = iframe['src']
        if src and match(r'^https?://', src):
            iframes.add(get_domain_from_url(src))

    anchors = set()
    for anchor in soup.find_all('a', href=True):
        href = anchor['href']
        if href and match(r'^https?://', href):
            anchors.add(get_domain_from_url(href))

    return {
        "javascripts": list(javascripts),
        "stylesheets": list(stylesheets),
        "images": list(images),
        "iframes": list(iframes),
        "anchors": list(anchors)
    }
