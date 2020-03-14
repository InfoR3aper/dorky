#!/bin/python3.7

from selenium import webdriver
import requests
import urllib
import os
import subprocess
import time
import sys
import random
from bs4 import BeautifulSoup

def mkdirs(path,exts_list):
    for ext in exts_list:
        try:
            ext = ext.replace('\n','')
            os.mkdir(path + "/" + ext + "/")
        except:
            print("")

def get_domain(doc_url):
    dom = doc_url.split('//')[1].replace('www.','')
    dom = dom.split('/')
    dom = dom[0]
    return dom

def get_gresults(ext,url,domdict,browser):
    browser.get(url)
    page_source  = browser.page_source

    if "unusual traffic" in page_source:
        print("unable to make http requests,aborting")
        sys.exit(0)
    soup = BeautifulSoup(page_source, 'lxml')
    tags = soup.find_all('a')
    for tag in tags:
        doc_url = str(tag.get('href'))
        if doc_url.startswith("http") or doc_url.startswith("https") or doc_url.startswith("ftp"):
            if not("google" in doc_url) and not("drive" in doc_url):
                domain = get_domain(doc_url)
                count = 0
                #print("downloading: " + doc_url)
                if not (domain in domdict):
                        domdict[domain] = 1
                        count = 1
                else:
                    domdict[domain] = domdict[domain] +1
                    count = domdict.get(domain)
                
                filename = domain + "_" + str(count)
                download(doc_url,filename)
                csv = open("log" + "_" + ext + ".csv","a")
                save_url(filename,doc_url,csv)
                csv.close()

def download(doc_url,filename):
   subprocess.call("wget  -q \"" + doc_url + "\" -O " + filename + "&>/dev/null" ,shell=True)

def save_url(filename,value,csv):
    csv.write(filename+ ";" + value + "\n")

def sleepr():
    sleep_time = random.randint(2,5)
    #print("sleepin " + str(sleep_time) +"s...")
    time.sleep(sleep_time)

def main():
    outputfolder = 'output'
    txtlist = open("filetypes.txt")
    file_ext = txtlist.readlines()
    g_URL = "https://www.google.com/search?q="
    dorks = ""
    query = ""
    print("insert your google dorks query")
    dorks = str(input())
    os.mkdir(outputfolder)
    os.chdir(outputfolder)
    path = os.path.abspath(os.getcwd())
    mkdirs(path,file_ext)
    firefox = webdriver.Firefox()
    for ext in file_ext:
        domdict = {}
        for page in range (0,9): #result pages:[1,10]
            page_attr = str(page * 10)
            os.chdir(path + "/" + ext + "/")
            query = urllib.parse.quote("(" + dorks + ") AND filetype:" + ext)
            url = g_URL + query + "&start="+page_attr
            print("doctype: " + ext + ",getting page " + str(page +1) + " results")
            get_gresults(ext,url,domdict,firefox)
            sleepr()
    os.chdir(path)

main()
