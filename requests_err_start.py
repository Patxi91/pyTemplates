# using the requests library to access internet data

import requests
from requests import HTTPError, Timeout


def main():
    # use requests to issue a standard HTTP GET request
    try:
        url = "http://httpbin.org/status/404"
        result = requests.get(url, timeout=2)
        result.raise_for_status()
        print_results(result)
    except HTTPError as err:
        print(f"Error: {err}")
    except Timeout as err:
        print(f"Request timed out: {err}")



def print_results(res_data):
    print(f"Result code: {res_data.status_code}")

    print("Headers: ------------------------")
    print(res_data.headers)

    print("Returned data: ------------------------")
    print(res_data.text)

main()
