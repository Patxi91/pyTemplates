# process JSON data returned from a server

import json


def main():
    # define a python dictionary
    python_data = {
            "sandwich": "Reuben",
            "toasted": True,
            "toppings": ["Thousand Island Dressing",
                         "Sauerkraut",
                         "Pickles"],
            "price": 8.99
    }

    # parse to JSON using dumps
    json_str = json.dumps(python_data, indent=4)

    # print the resulting JSON string
    print("JSON Data: ------------------")
    print(json_str)


main()
