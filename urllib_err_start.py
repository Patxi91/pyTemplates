# handling errors and status codes

import urllib.request
from http import HTTPStatus
from urllib.error import HTTPError, URLError


def main():

    url_a = "http://no-such-server.org"  # will generate an URLError
    url_b = "http://httpbin.org/status/404"  # will generate an HTTPError
    url_c = "http://httpbin.org/html"  # should work with no errors

    # use exception handling to attempt the URL access
    for url in [url_a, url_b, url_c]:
        print(url)
        try:
            result = urllib.request.urlopen(url)
            print(f"Result code: {result.status}")
            if result.getcode() == HTTPStatus.OK:
                print(result.read().decode('utf-8'))
        except HTTPError as err:
            print(f"Error: {err.code}")
            pass
        except URLError as err:
            print(f"That server is bunk. {err.reason}")

main()
