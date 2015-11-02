import urllib2


def load_page(url):
    """ Returns the content of the web page for a valid url.
        Otherwise it returns the empty string.
    """
    try:
        response = urllib2.urlopen(url)
        html = response.read()

        if response.code == 200:
            body_text = html
            return html
        return ""
    except Exception:
        return ""
