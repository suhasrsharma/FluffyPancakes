# -*- coding: utf-8 -*-
"""
@authors: Suhas Sharma and Rahul P
"""
"""
This class contains all the functions that are used multiple times in different methods in controller.py
Hence, it makes sense to call them once and re-use the values -> initialized in the __init__ method in controller.py

Error codes can be found at the end of this file
"""
import urllib.parse as urlparse
import whois 
import requests
from bs4 import BeautifulSoup as bs

class Recurrent:
    def checkURL(self, url):
        parts, url = Recurrent.partsHTTP(self, url)
        soup, resp = Recurrent.requests(self, url)
        if(resp==696):
            return False
        else:
            return True
        
    def parts(self, url): 
        parts = urlparse.urlsplit(url)
        if not parts.scheme and not parts.hostname:
            parts = urlparse.urlsplit("http://"+url)
        return parts
    
    def partsHTTP(self, url): 
        parts = urlparse.urlsplit(url)
        if not parts.scheme:
            url = 'http://' + url
        parts = urlparse.urlsplit(url)
        return parts, url
    
    def whois(self, url): 
        parts = urlparse.urlsplit(url)
        if not parts.scheme and not parts.hostname:
            parts = urlparse.urlsplit("http://"+url)
        domain_name = parts.netloc
        
        try:
            w = whois.whois(domain_name)
            try:
                w['domain_name']
            except:
                return 469
        
            if(w==None): 
                return 369
            if(w['domain_name']==None):
                return 800
            else:
                return w
        except:
            if(domain_name.count('.') > 1):
                try: 
                    w = whois.whois(domain_name[domain_name.index('.')+1:])
                    return w
                except:
                    return 345
                    
    def requests(self, url): 
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        headers = { 'User-Agent' : user_agent}
        try:
            resp = requests.get(url, headers=headers, timeout=3)
        except:
            return None, 696
        
        if(resp.status_code==200):
            soup = bs(resp.content, 'html.parser')
            return soup, resp
        else:
            return None, 707


#===Error Codes===
#-1 - Element not present
#0 - Legitimate
#1 - Phishing
#2 - Phishing: If the value set is (0,1,2)
#345 - Whois query did not return anything | Error
#505 - Error from Right Click Disabled
#369 - Whois query returned Null
#469 - Whois query does not have the field "domain_name"
#696 - requests.get(url) did not authorize the request
#707 - requests.status_code is not 200, can be anything else
#800 - .ai domain | Attributes in whois query are Null
#909 - Should never occur, technically. From If conditions and constraints.