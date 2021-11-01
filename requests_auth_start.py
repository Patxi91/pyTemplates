# using the requests library to access internet data

import requests
from requests.auth import HTTPBasicAuth

def main():
    # access an URL that requires authentication - Format: username/password to authenticate against
    url = "http://httpbin.org/basic-auth/PatxiOyaga/SecretPassword"

    # create a credentials object using HTTPBasicAuth
    my_creds = HTTPBasicAuth("PatxiOyaga", "SecretPassword")

    # issue the request with the authentication credentials
    result = requests.get(url, auth=my_creds)

    print_results(result)


def print_results(res_data):
    print(f"Result code: {res_data.status_code}")

    print("Headers: ------------------------")
    print(res_data.headers)

    print("Returned data: ------------------------")
    print(res_data.text)


main()
