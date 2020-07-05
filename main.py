import os
import csv
import json
import sys
import requests
import urllib
from urllib.request import Request, urlopen, HTTPError
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', required=True,help='Passing one url')
parser.add_argument('-p', '--pages', action='store_true', help='To download pages/post')
args = parser.parse_args()

url = args.url

if args.pages == True:
    url_link = url + "/wp-json/wp/v2/pages/?per_page=100"
else:
    url_link = url + "/wp-json/wp/v2/posts/?per_page=100"

try:
    req = Request(url_link, headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()



    ## Fetching hostname of the URL
    from urllib.parse import urlparse
    parsed_uri = urlparse(url_link)
    result = '{uri.netloc}'.format(uri=parsed_uri)

    # Write data to file
    filename = "data/" + result + "-raw_data.txt"
    file_ = open(filename, 'wb')
    file_.write(webpage)
    file_.close()


    with open(filename) as json_file:
        json_data = json.load(json_file)

    C_data = []

    for n in json_data:  
    
        r={}
        r["Modified"] = n['modified']
        r["Title"] = n['title']['rendered']
        r["Content"] = n['content']['rendered']
        r["Link"] = n['link']

        # JSON Conversion

        j_data = {
            "modified/posted" : r["Modified"],
            "title" : r["Title"],
            "content" : r["Content"],
            "link" : r["Link"]
        }

        C_data.append(j_data)
        print("Title: " + r["Title"])
        print("Status: Downloaded")
        
    json_object = json.dumps(C_data, indent = 4) 

    # Writing to sample.json 
    with open("data/" + result + "-data.json", "w") as outfile: 
        outfile.write(json_object)
    print("Extracted Successfully")
    
except urllib.error.HTTPError as e:
    ResponseData = e.read().decode("utf8", "ignore")
    print(e)
except IndexError:
    print("No input detected!")     