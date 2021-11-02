# use the lxml library to parse a document in memory

import requests
from lxml import etree


def main():
    # retrieve the XML data using the requests library
    url = "http://httpbin.org/xml"
    result = requests.get(url)

    # build a doc structure using the ElemntTree API
    doc = etree.fromstring(result.content)  # expects bite content
    print(result.text)

    # access the value of an attribute
    print(doc.tag)
    print(doc.attrib['title'])

    # iterative over tags
    for elem in doc.findall("slide"):
        print(elem.tag)

    slide_count = len(doc.findall("slide"))
    print(f"There are {slide_count} slide elements.")

    # create a new slide
    new_slide = etree.SubElement(doc, "slide")
    new_slide.text = "This is a new slide"

    # count the number of slides
    slide_count = len(doc.findall("slide"))
    item_count = len(doc.findall(".//item"))

    print(f"There are {slide_count} slide elements.")
    print(f"There are {item_count} item elements.")


main()
