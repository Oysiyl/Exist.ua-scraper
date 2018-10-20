#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 13:56:38 2018

@author: dmitriy
"""

#import all the necessary libraries
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests

#Create function that scraping full one page from site
print("Parsing will be complete in three stages")
start0 = time.time()
print("Begins")
adres2 = "https://exist.ua/unicat/cars/abarth/"

def secondlevel(url):
    #Use headers to prevent hide our script
    headers = {'User-Agent': 'Mozilla/5.0'}
    #Get page
    page = requests.get(url, headers = headers)
    #Get all of the html code 
    soup = BeautifulSoup(page.content, 'html.parser')
    #Find title the topic
    list0=[]
    possible_links = soup.find_all('a')
    for link in possible_links:
        if link.has_attr('href'):
            #print (link.attrs['href'])
            list0.append(link.attrs['href'])
    matching = [s for s in list0 if "/unicat/cars/" in s]
    title = matching
    preparetitle = []
    for i in range(len(title)):
        k = "https://exist.ua/" + str(title[i])
        preparetitle.append(k)
        prep = []
    for i in range(len(preparetitle)):
        #Use headers to prevent hide our script
        headers = {'User-Agent': 'Mozilla/5.0'}
        #Get page
        page = requests.get(preparetitle[i], headers = headers)
        #Get all of the html code 
        soup = BeautifulSoup(page.content, 'html.parser')
        #Find title the topic
        pip = []
        possible_links = soup.find_all('a')
        for link in possible_links:
            if link.has_attr('href'):
                #print (link.attrs['href'])
                pip.append(link.attrs['href'])
        pip = [s for s in pip if str(title[i]) in s]
        prep.extend(pip)
    prep = list(set(prep))
    preparetitle2 = []
    for i in range(len(prep)):
        k = "https://exist.ua/" + str(prep[i])
        preparetitle2.append(k)
    prep = preparetitle2
    return prep

adres3 = "https://exist.ua/unicat/cars/"

def firstlevel(url):
    #Use headers to prevent hide our script
    headers = {'User-Agent': 'Mozilla/5.0'}
    #Get page
    page = requests.get(url, headers = headers)
    #Get all of the html code 
    soup = BeautifulSoup(page.content, 'html.parser')
    #Find title the topic
    list0=[]
    possible_links = soup.find_all('a')
    for link in possible_links:
        if link.has_attr('href'):
            #print (link.attrs['href'])
            list0.append(link.attrs['href'])
    matching = [s for s in list0 if "/unicat/cars/" in s]
    title = matching
    preparetitle = []
    for i in range(len(title)):
        k = "https://exist.ua/" + str(title[i])
        preparetitle.append(k)
        u = 100/len(title)
        percent = round(i*u,2)
        print(percent)
    prep = preparetitle[1:]
    return prep

start1 = time.time()
test2 = firstlevel(adres3)
end1 = time.time()
elapsed_time1 = end1 - start1
elapsed_time1 = time.strftime("%H:%M:%S", time.gmtime(elapsed_time1))
print("First stage took " + str(elapsed_time1))
list3 = []
start2 = time.time()
for i in range(len(test2)):
    k = secondlevel(test2[i])
    list3.extend(k)
    u = 100/len(test2)
    percent = round(i*u,2)
    print(percent)
end2 = time.time()
elapsed_time2 = end2 - start2
elapsed_time2 = time.strftime("%H:%M:%S", time.gmtime(elapsed_time2))
print("Second stage took " + str(elapsed_time2))

def table(url):
    #Use headers to prevent hide our script
    headers = {'User-Agent': 'Mozilla/5.0'}
    #Get page
    page = requests.get(url, headers = headers)
    #Get all of the html code 
    soup = BeautifulSoup(page.content, 'html.parser')
    #Find title the topic
    title = soup.find("div", class_ = "car-modification-name")
    title = title.get_text()
    html = requests.get(adres).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    df["Автомобиль"] = title
    #print(df)
    return df

listtest = ['https://exist.ua//unicat/cars/alpine/1300/1300-2420/', 'https://exist.ua//unicat/cars/alpine/a310/a310-2421/', 'https://exist.ua//unicat/cars/alpine/berlinette/berlinette-2422/', 'https://exist.ua//unicat/cars/alpine/v6/v6-4298/', 'https://exist.ua//unicat/cars/alpine/1600/1600-4738/', 'https://exist.ua//unicat/cars/alpine/a610/a610-2423/', 'https://exist.ua//unicat/cars/alpine/a110/a110-2419/']
#Create an empty DataFrame
df = pd.DataFrame()
#Adding each new page in one DataFrame
start3 = time.time()
for url in range(len(list3)):
    df = pd.concat([df, table(list3[url])], ignore_index = True)
    u = 100/len(list3)
    percent = round(url*u,2)
    print(percent)
end3 = time.time()
elapsed_time3 = end3 - start3
elapsed_time3 = time.strftime("%H:%M:%S", time.gmtime(elapsed_time3))
print("Third stage took " + str(elapsed_time3))
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]
#Save DataFrame to csv
df.to_csv("auto.csv")    

adres = "https://exist.ua/unicat/cars/abarth/500-595/500-595-312-18523/"
end0 = time.time()
elapsed_time0 = end0 - start0
elapsed_time0 = time.strftime("%H:%M:%S", time.gmtime(elapsed_time0))
print("Mission complete in " + str(elapsed_time0))
