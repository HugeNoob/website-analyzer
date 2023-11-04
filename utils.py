from urllib.parse import urlparse


def get_url_with_scheme(url):
    if not url.startswith("https://") or url.startswith("http://"):
        url = "https://" + url
    return url


def get_domain_from_url(url, keep_www=True):
    if not url.startswith("https://"):
        url = "https://" + url

    domain = urlparse(url).netloc
    if keep_www:
        return domain

    parts = domain.split('.')
    if parts[0] == "www":
        return ".".join(parts[1:])

    return domain
