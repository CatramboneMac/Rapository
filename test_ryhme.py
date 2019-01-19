#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 12:14:14 2019

@author: ErichHairston
"""

from lxml import html
import requests
import csv ##
def word_2_rhyme():
    word=input("Input a word to rhyme with, q to quit: ")
    if(word.lower()=="q"):
        return "q"
    else:
        
        word_dict=GetRhymes(str(word))
        display(word,word_dict)
        return word
    
def GetRhymes(in_word):
    """
    Given a word, scrapes the web (Rhymezone.com), to find words that rhyme with it.
    Returns a set of words that rhymes.
    """
    word_L=[]
    word_dict={}
    if(" "in in_word):
        in_word=in_word.replace(" ","+")
    url_string = "https://www.rhymezone.com/r/rhyme.cgi?Word=" + str(in_word.lower()).strip() + "&typeofrhyme=perfect&org1=syl&org2=l&org3=y"
    url_string = str(url_string)
    page = requests.get(url_string)
    tree = html.fromstring(page.content)
    rhymes = tree.xpath('//b//a[@class="r"]/text()')
    for word in rhymes:
        if("\xa0"in word):
            word=word.replace("\xa0"," ")
        word_L.append(word)
    word_dict[in_word]=word_L
    write_file(word_dict)
    return word_dict
def write_file(word_dict):
    with open("EZR.csv","a") as csv_file:
        writer = csv.writer(csv_file)
        for key,value in word_dict.items():
                writer.writerows([value])
def DB_check(in_word):
    word_dict={}
    with open("EZR.csv","r") as csv_file:
        reader=csv.reader(csv_file)
    for line in reader:
        word_list=line.split(",").strip().lower()
        if (in_word.lower() in word_list):
            word_dict[in_word]= word_list
        if (in_word.strip().lower() not in word_list):
            word_dict=GetRhymes(in_word)
            
    return word_dict
def display(word,word_dict):
    print("List of words that rhyme with {:s}".format(word))
    for key,value in word_dict.items():
        for item in value:
            print(item)
    
def main():
    ans="start"
    while(ans.lower()!="q"):
        ans=word_2_rhyme()
        if(ans=="q"):
            break
        

    
if __name__ == "__main__":
    main()