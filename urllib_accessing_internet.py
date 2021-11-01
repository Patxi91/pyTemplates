# using urllib to request data

import urllib.request


def main1():
    # the URL to retrieve our sample data from
    url = "http://httpbin.org/xml"

    # open the URL and retrieve some data
    result = urllib.request.urlopen(url)

    # print the result code from the request, should be 200 OK
    print(f"Result code: {result.status}")

    # print the returned data headers
    print("Headers: ------------------------")
    print(result.getheaders())

    # print the returned data itself
    print("Returned data: ------------------------")
    print(result.read().decode('utf-8'))

# Drivers
main1()
