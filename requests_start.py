# using the requests library to access internet data

import requests

def main():
    # use requests to issue a standard HTTP GET request
    url = "http://httpbin.org/xml"
    result = requests.get(url)
    print_results(result)

    # send some parameters to the URL via a GET request, requests handles it automatically
    url = "http://httpbin.org/get"
    data_values = {
        "key1": "value1",
        "key2": "value2"
    }
    result = requests.get(url, params=data_values)
    print_results(result)

    # send some parameters to the URL via a POST request, requests handles it automatically
    url = "http://httpbin.org/post"
    data_values = {
        "key1": "value1",
        "key2": "value2"
    }
    result = requests.post(url, data=data_values)
    print_results(result)


    # pass a custom header to the server
    url = "http://httpbin.org/get"
    header_values = {
        "User-Agent": "Joe Marini App / 1.0.0"
    }
    result = requests.get(url, headers=header_values)
    print_results(result)


def print_results(res_data):
    print(f"Result code: {res_data.status_code}")

    print("Headers: ------------------------")
    print(res_data.headers)

    print("Returned data: ------------------------")
    print(res_data.text)

main()
