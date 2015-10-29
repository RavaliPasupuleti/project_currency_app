import urllib2


def load_page(url):
    """ Returns the content of the web page for a valid url.
        Otherwise it returns the empty string.
    """
    try:
        response = urllib2.urlopen(url)
        html = response.read()

        if response.status == 200:
            body_text = str(response.read())
            return body_text
        return ""
    except Exception:
        return ""
