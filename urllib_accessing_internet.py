# using urllib to request data

import urllib.request
import urllib.parse


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


def main2():
    # the URL to retrieve our sample data from
    url = "http://httpbin.org/get"

    # create some data to pass to the GET request
    args = {
        "name": "Patxi Oyaga",
        "is_author": True
    }

    # the data needs to be url-encoded before passing as arguments
    data = urllib.parse.urlencode(args)

    # issue the request with the data parameters as part of the URL
    result1 = urllib.request.urlopen(url + "?" + data)  # data goes in args

    print(f"Result code: {result1.status}")
    print("Returned data: ------------------------")
    print(result1.read().decode('utf-8'))

    # issue the request with a data parameter to use POST
    url = "http://httpbin.org/post"
    data = data.encode()
    result2 = urllib.request.urlopen(url, data=data)  # data goes in form (POST)

    print(f"Result code: {result2.status}")
    print("Returned data: ------------------------")
    print(result2.read().decode('utf-8'))


# Drivers
main1()
main2()
