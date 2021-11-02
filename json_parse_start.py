# process JSON data returned from a server

import json


def main():
    # define a string of JSON code
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
    data = json.loads(json_str)

    # print information from the data structure
    print("Sandwich: " + data["sandwich"])
    if data["toasted"]:
        print("And it's toasted!")
    for topping in data["toppings"]:
        print("Topping: " + topping)


main()
