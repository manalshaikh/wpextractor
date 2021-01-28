import os
import csv
import json
import sys
import requests
import urllib
from urllib.request import Request, urlopen, HTTPError
from urllib.parse import urlparse
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='To mention file')
parser.add_argument('-u', '--url', help='Passing one url')
parser.add_argument('-p', '--pages', action='store_true', help='To download pages/post')
args = parser.parse_args()


def get_urls(filename):
    urls = []

    file = open(filename, "r")

    for i in file:
        i = i.replace("\n", "")
        urls.append(i)
    return urls

def get_data_url(url_link):
    req = Request(url_link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    ## Fetching hostname of the URL
    parsed_uri = urlparse(url_link)
    result = '{uri.netloc}'.format(uri=parsed_uri)
    print(result)
    # Write data to file
    filename = "data/" + result + "-raw.txt"
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
    
   
try:
    option = sys.argv[1]
    if option == "-f":
        urls = get_urls(args.file)
        urls = list(urls)
        for i in urls:
            if args.pages == True:
                i = i + "/wp-json/wp/v2/pages/?per_page=100"
            else:
                i = i + "/wp-json/wp/v2/posts/?per_page=100"
            try:
                get_data_url(i)
            except urllib.error.HTTPError as e:
                ResponseData = e.read().decode("utf8", "ignore")
                print(e)

    else:
        try:
            url = args.url
            if args.pages == True:
                url = url + "/wp-json/wp/v2/pages/?per_page=100"
            else:
                url = url + "/wp-json/wp/v2/posts/?per_page=100"
            get_data_url(url)
        except urllib.error.HTTPError as e:  # Error handling begins
            ResponseData = e.read().decode("utf8", "ignore")
            fcode = e.code
            if fcode == 404:
                print("Ops! The URL you supplied is not a WordPress URL. Please check for any typo and try again.")
            if fcode == 403:
                print("The URL you are trying to locate is forbidden.")
            if fcode == 401:
                print("The URL you are trying to access has marked you unauthorized.")
            if fcode == 408:
                print("The URL you are trying to access has timed out.")
            if fcode == 500:
                print("The URL you are trying to access has returned Internal Server Access.")
            if fcode == 502:
                print("The URL you are trying to access has returned Bad Gateway error.")

except IndexError:
    print("No arguments passed! use -h to check all commands")     