# process JSON data returned from a server

import json
from json import JSONDecodeError


def main():
    # define a string of JSON code
    # removing a comma --> json.decoder.JSONDecodeError: Expecting ',' delimiter --> need error  handling
    json_str = '''{
            "sandwich" : "Reuben",
            "toasted" : true,
            "toppings" : [
                "Thousand Island Dressing",
                "Sauerkraut",
                "Pickles"
            ],
            "price" : 8.99
    }'''

    # parse the JSON data using loads
    try:
        data = json.loads(json_str)
    except JSONDecodeError as err:
        print("JSON decoding error:")
        print(err.msg)
        print(err.lineno, err.colno)


    # print information from the data structure
    print("Sandwich: " + data["sandwich"])
    if data["toasted"]:
        print("And it's toasted!")
    for topping in data["toppings"]:
        print("Topping: " + topping)


main()
