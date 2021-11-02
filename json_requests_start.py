# using the requests library to access internet data

import requests
import json


def main():
    # use requests to issue a standard HTTP GET request
    url = "http://httpbin.org/json"
    result = requests.get(url)

    # use built-in JSON function to return parsed data
    data_obj = result.json()
    print(json.dumps(data_obj, indent=4))

    # access data in the python object
    print(list(data_obj.keys()))

    print(data_obj["slideshow"]["title"])
    print(f"There are {len(data_obj['slideshow']['slides'])} slides")


main()
