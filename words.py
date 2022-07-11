################################################################
######
###### Program to Fetch page and report the top n words  
###### Author  : Gokularaman R                          
###### Date    : 7/11/2022                               
###### Version : 1.0    
###### History : 2022-07-11  - GR - Initial Version
######                                 
################################################################
import requests
import json
import sys
import getopt
from collections import OrderedDict
import unittest

n=5
page_id=21721040

def top_words(n,page_id):
    URL = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&pageids={page_id}&explaintext&format=json"

    data = requests.get(url = URL).json()
    title     = data['query']['pages'][str(page_id)]['title']
    page_text = data['query']['pages'][str(page_id)]['extract']


    counts = {}			
    def word_count(str):
        words = str.split()
        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        return counts

    word_count(page_text)

    dict4 = {k:v for (k,v) in counts.items() if len(k) >= 4}
    final_dict = {k:v for (k,v) in dict4.items() if k[0:4].isalpha() } 


    flipped = {}
    for key, value in final_dict.items():
        if value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)

    dict1 = OrderedDict(sorted(flipped.items()))
    sorted_dict = sorted(dict1.items(), key=lambda x: x[0], reverse=True)


    t=f"Title: {title}"
    n_w=f"Top {n} words:"
    final_output =[t,n_w]
    x = 0
    for i in sorted_dict:
        if x == n:
            break
        else:
            v = "{0} {1}".format(i[0], ','.join(i[1]))
            final_output.append(v)
            x += 1
    print( "\n".join(final_output))
    return "\n".join(final_output)
top_words(n,page_id)



class MyTest(unittest.TestCase):
    def test_top_5_words(self):
        w ="""Title: Stack Overflow
Top 5 words:
18 Stack
15 questions
14 Overflow
11 that
9 users"""
        self.assertEqual(top_words(5,21721040), w)

    def test_top_3_words(self):
        w ="""Title: Stack Overflow
Top 3 words:
18 Stack
15 questions
14 Overflow"""
        self.assertEqual(top_words(3,21721040), w)

    def test_top_6_words(self):
        w ="""Title: Stack Overflow
Top 6 words:
18 Stack
15 questions
14 Overflow
11 that
9 users
8 only"""
        self.assertEqual(top_words(6,21721040), w)