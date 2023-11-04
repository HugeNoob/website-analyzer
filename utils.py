from urllib.parse import urlparse


def get_url_with_scheme(url):
    """
    Adds the https:// scheme to a URL if it does not already have one

    Parameters
    ----------
    url : str
        URL to add the scheme to

    Returns
    -------
    str
        URL with the scheme added
    """

    if not url.startswith("https://") or not url.startswith("http://"):
        url = "https://" + url
    return url


def get_domain_from_url(url, keep_www=True):
    """
    Extracts the domain from a URL

    Parameters
    ----------
    url : str
        URL to extract the domain from

    keep_www : bool, optional
        Whether to keep the www prefix in the domain

    Returns
    -------
    str
        Domain extracted from the URL
    """

    url = get_url_with_scheme(url)

    domain = urlparse(url).netloc
    if keep_www:
        return domain

    parts = domain.split('.')
    if parts[0] == "www":
        return ".".join(parts[1:])

    return domain
