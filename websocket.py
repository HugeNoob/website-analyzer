from utils import get_url_with_scheme

from analyzer import extract_domain_info, extract_subdomains, extract_asset_domains


def process_message(msg, analyzed_information):
    if "url" in msg:
        recv_url = msg["url"]
        url_with_scheme = get_url_with_scheme(recv_url)

        analyzed_information["info"] = extract_domain_info(url_with_scheme)
        analyzed_information["subdomains"] = extract_subdomains(
            url_with_scheme)
        analyzed_information["asset_domains"] = extract_asset_domains(
            url_with_scheme)

        resp = {"data": f'session created for {recv_url}'}

    elif "operation" in msg:
        op = msg["operation"]

        if op == "get_info":
            info = analyzed_information["info"]
        elif op == "get_subdomains":
            info = analyzed_information["subdomains"]
        elif op == "get_asset_domains":
            info = analyzed_information["asset_domains"]
        else:
            info = "Could not interpret your query."

        resp = {"data": info}
    else:
        resp = {"data": "Could not interpret your query."}

    return resp
