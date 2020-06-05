# -*- coding: utf-8 -*-
"""
@authors: Suhas Sharma and Rahul P
"""

"""
Error codes can be found at the end of this file
"""

import ipaddress as ip
import urllib.parse as urlparse
import ssl
import socket
import requests
from bs4 import BeautifulSoup as bs
from ast import literal_eval 
import urllib
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

from recurrent import Recurrent

class Controller:
    def __init__(self, url):
        self.url = url
        self.IP = False
        
        # Calling the recurrent functions
        instance = Recurrent()
        self.validURL = instance.checkURL(url)
        self.parts = instance.parts(url)
        self.partsHTTP, url_new = instance.partsHTTP(url)
        self.url_new = url_new
        self.w = instance.whois(url)
        self.soup, self.resp = instance.requests(url_new)
    
    # Extracting the features as listed in the UCI Dataset
    # Note that 23 out of 30 features have been used 
    def checkValidURL(self):
        validURL = self.validURL
        Controller.havingIPAddress(self)
        if(validURL==True or self.IP==True):
            return True
        elif(validURL==False or self.IP==False):
            return False
        
    def havingAtSymbol(self):
        parts = self.parts
        url = self.url
        if('@' in parts.netloc):
            output = 1
            url = url[url.find('@'):]
            self.url = url
        else:
            output = 0
        return output
    
    def doubleSlashRedirection(self):
        parts = self.parts
        if('//' in parts.path):
            self.url = parts.path[2:]
            return 1
        else:
            return 0
    
    def havingIPAddress(self):
        url = self.url
        if('http://' in url):
            parts = urlparse.urlsplit(url)
            url = parts.hostname
        if('0x' in url):
            unmasked_url = ''
            IP = url.split('.')
            for hexa in IP:
                unmasked_url = unmasked_url + '.' + str(literal_eval(hexa))
            url = unmasked_url[1:]
        try:
            ip.ip_address(url)
            self.IP = True
            return 1
        except ValueError:
            return 0
        
    def lengthOfURL(self):
        url = self.url
        url_length = len(url)
        if (url_length < 54):
            return 0
        elif(url_length>=54 and url_length<=75):
            return 1
        else:
            return 2
        
    def shorteningService(self):
        url = self.url
        short_url, long_url = url, ''
        test_read = open(r'./data/shortening_services.txt', 'r')
        
        havingIP = Controller.havingIPAddress(self)
        
        #To get the proper shortened URL and convert it to a regular long URL; second parameter -> if URL not an IP
        if((('http://' or 'https://') not in url) and (havingIP!=1)):
            short_url = 'http://' + url
        
        #The following operations require the URL to be a string. Checking that it isn't hexadeimal or decimal
        if(havingIP==0):
            parts = self.parts
            shortening_service = bool(parts.netloc in test_read.read() and parts.path)
            if(shortening_service):
                #Find the original long URL
                session = requests.Session()
                resp = session.head(short_url, allow_redirects=True)
                long_url = resp.url
                return 1
                self.url = long_url
            else:
                return 0
                self.url = url
        else:
            self.url = url
            return 0
        
    def prefixSuffix(self):
        parts = self.parts        
        if('//' not in parts.path):
            if('-' in parts.netloc):
                return 1
            else:
                return 0
            return
        
        elif('//' in parts.path):
            if('-' in parts.path[2:]):
                return 1
            else: 
                return 0
    
    def havingSubDomain(self):
        parts = self.parts
        havingIP = Controller.havingIPAddress(self)
        #Handling if IP case
        if(havingIP!=1):
            if('www' in parts.netloc):
                if(str(parts.netloc).count('.')>3):
                    return 2
                elif(str(parts.netloc).count('.')>2):
                    return 1
                else:
                    return 0
            else:
                if(str(parts.netloc).count('.')>2):
                    return 2
                elif(str(parts.netloc).count('.')>1):
                    return 1
                else:
                    return 0
        else:
            return 0
    
    def SSLFinalState(self):
        havingIP = Controller.havingIPAddress(self)
        if(havingIP==1):
            return 1
        else:
            parts = self.partsHTTP
            CA = ''
            hostname = parts.netloc
            try:
                ctx = ssl.create_default_context()
                s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
                s.settimeout(3)
                s.connect((hostname, 443))
                cert = s.getpeercert()
            except:
                return 1
            issuer = dict(x[0] for x in cert['issuer'])
            issued_by = issuer['commonName']
            if(len(issued_by.split(" "))>1):
                CA = issued_by.split(" ")[0] + " " + issued_by.split(" ")[1] 
            
            SSL_read = open(r'./data/ssl_list.txt','r')
            
            if((issued_by.split()[0] or CA)in SSL_read.read()):
                return 0
            else:
                return 1
    
    def domainRegistration(self):
        test_read = open(r'./data/edu_domains.txt', 'r')
        parts = self.parts
        domain_name = parts.netloc
        if('.edu' in domain_name):
            if(domain_name in test_read.read()):
                return 0 
            else:
                return 1
        else:
            w = self.w
            if(w==800 ):
                return 800
            elif(w==369 or w==345 or w==469):
                return 1
            else:
                try:
                    if(type(w['expiration_date']) == list and type(w['creation_date']) == list):
                        days_alive = w['expiration_date'][0] - w['creation_date'][0]
                    else:
                        days_alive = w['expiration_date']-w['creation_date']
                    days_alive = int(str(days_alive).split(" ")[0])
                except TypeError:
                    days_alive = 0
            if(days_alive > 365):
                return 0
            else:
                return 1
            
    def faviconCheck(self):
        parts = self.partsHTTP
        soup = self.soup
        resp = self.resp
        
        if(resp==696):
            return 696
        elif(resp==707):
            return 707
        else:
            head = soup.find('head')
        
        if(head!=None):
            if(head.find(rel = "shortcut icon")):
                favicon = head.find(rel = "shortcut icon")
            elif(head.find(rel = "icon")):
                favicon = head.find(rel = "icon")
            else: 
                favicon = None
            
            if(favicon!=None):
                href = favicon.get('href')
                parts_href = urlparse.urlsplit(href)
                
                if(parts_href.scheme):
                    if(parts.netloc == parts_href.netloc): 
                        return 0
                    else:
                        return 1
                else:
                    return 0
                
            else:
                return 1
                    
        else:
            return 1
    
    def openPorts(self):
        #Port 20: FTP
        #Port 21: FTP
        #Port 22: SSH
        #Port 23: Telnet
        #Port 25: SMTP
        #Port 53: DNS
        #Port 67: DHCP
        #Port 68: UDP
        #Port 110: POP3
        #Port 143: IMAP
        #Port 445: SMB
        #Port 1433: MSSQL
        #Port 1521: Oracle
        #Port 3306: MySQL
        #Port 3389: Remote Desktop
        
        ports = [20, 21, 22, 23, 25, 53, 67, 68, 110, 143, 445, 1433, 1521, 3306, 3389]
        open_ports = []
        validURL = True
        
        parts = self.parts
        
        for port in ports:
            domain_name = (parts.netloc, port)
            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            a_socket.settimeout(1)
            try: 
                result = a_socket.connect_ex(domain_name)
            except:
                validURL = False
                return 1
                break
            if(result==0):
                open_ports.append(port)
                break
            else:
                pass
            a_socket.close()
        
        if(validURL==True):    
            if(open_ports):
                return 1
            else:
                return 0
            
    def httpsToken(self):
        parts = self.parts
        if('https' in parts.hostname):
            return 1
        else:
            return 0
    
    #Inner function for requestURL
    def get_videos(url, outYouTubeCount, totalYouTubeCount): 
        try:
            request = urllib.request.Request(url)
            opener = urllib.request.build_opener()
            page = opener.open(request)
            soup = bs(page, 'lxml')
        except:
            return outYouTubeCount, totalYouTubeCount
    
        title = soup('title')[0].string
        videoids = []
        for element in soup('embed'):
            src = element.get('src')
            if(src!=None):
                if re.search('v\/([-\w]+)', src):
                    outYouTubeCount += 1
                    totalYouTubeCount += 1
                    videoids.append(re.search('v\/([-\w]+)', src).group(1))
        for element in soup('iframe'):
            src = element.get('src')
            if(src!=None):
                if re.search('youtube.com\/embed\/', src):
                    outYouTubeCount += 1
                    totalYouTubeCount += 1
                    videoids.append(re.search('embed\/([-\w]+)', src).group(1))
        for element in soup('a'):
            href = element.get('href')
            if href and re.search('youtube.com\/watch\?v=([-\w]+)', href):
                outYouTubeCount += 1
                totalYouTubeCount += 1
                videoids.append(re.search('youtube.com\/watch\?v=([-\w]+)', href).group(1))
            if href and re.search('youtu\.be\/([-\w]+)', href):
                outYouTubeCount += 1
                totalYouTubeCount += 1
                videoids.append(re.search('youtu\.be\/([-\w]+)', href).group(1))
    
        res = {}
        res['title'] = title
        res['videoids'] = list(set(videoids))
        return outYouTubeCount, totalYouTubeCount
    
    def requestURL(self):
        inImageCount = 0
        inVideoCount = 0
        inVidCount = 0
        outImageCount = 0
        outVidCount = 0
        outVideoCount = 0
        outYouTubeCount = 0
        totalYouTubeCount = 0
        totalCount = 0
        images = []
        vids = []
        videos = []
        
        parts = self.partsHTTP
        url = self.url_new
        resp = self.resp
        soup = self.soup
        
        try:
            outYouTubeCount, totalYouTubeCount = Controller.get_videos(url, outYouTubeCount, totalYouTubeCount)
            totalCount += totalYouTubeCount
        except IndexError:
            #print("The inner function is causing some issue: title[0] - index out of range")
            pass
            
        if(resp==696):
            return 696
        elif(resp==707):
            return 707
        else:
            images = soup.find_all('img')
            vids = soup.find_all('vid')
            videos = soup.find_all('video')
        
        if(len(images)!=0):
            for i in images:
                if(i.get('src')):
                    image = i.get('src')
                elif(i.get('data-delayed-url')):
                    image = i.get('data-delayed-url')
                try:
                    parts_image = urlparse.urlsplit(image)
                    if(parts_image.scheme):
                        if(parts.hostname != parts_image.hostname):
                            outImageCount += 1
                            totalCount += 1
                    else:
                        inImageCount += 1
                        totalCount += 1
                except:
                    pass
        else:
            pass
        
        if(len(vids)!=0):
            for i in vids:
                if(i.get('src')):
                    vid = i.get('src')
                parts_vid = urlparse.urlsplit(vid)
                if(parts_vid.scheme):
                    if(parts.hostname != parts_vid.hostname):
                        outVidCount += 1
                        totalCount += 1
                else:
                    inVidCount += 1
                    totalCount += 1
        else:
            pass
        
        if(len(videos)!=0):
            for i in videos:
                if(i.get('src')):
                    video = i.get('src')
                parts_video = urlparse.urlsplit(video)
                if(parts_video.scheme):
                    if(parts.hostname != parts_video.hostname):
                        outVideoCount += 1
                        totalCount += 1
                else:
                    inVideoCount += 1
                    totalCount += 1
        else:
            pass
        
        
        if(totalCount!=0):
            ratio = (outImageCount+outVidCount+outVideoCount+outYouTubeCount)/totalCount
            if(ratio<0.22):
                return 0
            elif((ratio>=0.22) and (ratio<0.61)):
                return 1
            elif(ratio>=0.61 and ratio<=1):
                return 2
            else:
                return 909
        else:
            return 0

        
    def urlOfAnchor(self):
        anchorCount = 0
        anchorNoLinkCount = 0
        tag = []
        
        resp = self.resp
        soup = self.soup
        
        if(resp==696):
            return 696
        elif(resp==707):
            return 707
        else:
            tag = soup.find_all('a')
        
        if(len(tag)!=0):
            for i in tag:
                aTag = i.get('href')
                if(aTag=='#'):
                    anchorNoLinkCount += 1
                elif(aTag=='#content'):
                    anchorNoLinkCount += 1
                elif(aTag=='#skip'):
                    anchorNoLinkCount += 1
                elif(aTag=='JavaScript ::void(0)'):
                    anchorNoLinkCount += 1
                anchorCount += 1
        
            if((anchorNoLinkCount/anchorCount)<0.31):
                return 0
            elif((anchorNoLinkCount/anchorCount)>= 0.31 and (anchorNoLinkCount/anchorCount)<0.67):
                return 1
            elif((anchorNoLinkCount/anchorCount)>=0.67 and (anchorNoLinkCount/anchorCount)<=1):
                return 2
            else: 
                return 909
        else:
            return 0
        
        
    def linksInTags(self):
        totalTags = 0
        metaTags = 0
        scriptTags = 0
        linkTags = 0
        meta = []
        script =[]
        link = []
        
        parts = self.partsHTTP
        resp = self.resp
        soup = self.soup
        
        if(resp==696):
            return 696
        elif(resp==707):
            return 707
        else:
            meta = soup.find_all('meta')
            script = soup.find_all('script')
            link = soup.find_all('link')
        
        if(len(meta)!=0):
            for m in meta:
                if(m.get('url')):
                    parts_meta = urlparse.urlsplit(m.get('url'))
                    if(parts_meta.scheme):
                        if(parts_meta.netloc != parts.netloc):
                            metaTags += 1
                    totalTags += 1
        else:
            pass
        
        if(len(script)!=0):
            for s in script:
                if(s.get('src')):
                    parts_script = urlparse.urlsplit(s.get('src'))
                    if(parts_script.scheme):
                        if(parts_script.netloc != parts.netloc):
                            scriptTags += 1
                    totalTags += 1
        else:
            pass
           
        if(len(link)!=0):
            for l in link:
                if(l.get('href')):
                    parts_link = urlparse.urlsplit(l.get('href'))
                    if(parts_link.scheme):
                        if(parts_link.netloc != parts.netloc):
                            linkTags += 1
                    totalTags += 1
        else:
            pass
        
        if(totalTags!=0):
            ratio = (metaTags+scriptTags+linkTags)/totalTags
            if(ratio<0.17):
                return 0
            elif(ratio>=0.17 and ratio<=0.81):
                return 1
            elif(ratio>0.81 and ratio<=1):
                return 2
            else:
                return 909
        else:
            return 0  
        
        
    def SFH(self):
        sfh = []
        phishing = 0
    
        parts = self.partsHTTP
        resp = self.resp
        soup = self.soup
        
        if(resp==696):
            return 696
        elif(resp==707):
            return 707
        else:
            sfh = soup.find_all('form')

        if(len(sfh)!=0):
            for f in sfh:
                action = f.get('action')
                parts_action = urlparse.urlsplit(action)
                if(action==None or action=="" or action=="about:blank"):
                    phishing = 2
                    break
                elif(parts_action.scheme):
                    if(parts.hostname != parts_action.hostname):
                        phishing = 1
                        break
                elif(action.startswith('/')):
                    phishing = 0
                    break
            if(phishing==0):
                return 0
            elif(phishing==1):
                return 1
            elif(phishing==2):
                return 2
        else:
            return 0
        
    def submittingToMail(self):
        aTag = []
        mailTo = False
        
        resp = self.resp
        soup = self.soup
        
        if(resp==696):
            return 696
        elif(resp==707):
            return 707
        else:
            if('mailto:' in resp.text):
                mailTo=True
            aTag = soup.find_all('a')

        if(len(aTag)!=0):
            for a in aTag:
                href = a.get('href')
                if(href!=None):
                    if('mailto:' in href):
                        mailTo = True
            if(mailTo == True): 
                return 1
            else:
                return 0
        else:
            return 0
        
    def abnormalURL(self):
        domain_name = self.parts.netloc
        w = self.w
        if(w==800):
            return 800
        elif(w==369 or w==345 or w==469):
            return 1
        else:
            whois_domain_name = w['domain_name']
            if(type(whois_domain_name)==str):
                if(whois_domain_name.lower() in domain_name):
                    return 0
                else:
                    return 1
            elif(type(whois_domain_name)==list):
                if(whois_domain_name[1].lower() in domain_name):
                    return 0
                else:
                    return 1
                
    def websiteForwarding(self):
        redirectCount = 0
        
        resp = self.resp
        
        if(resp==696):
            return 696
        elif(resp==707):
            return 707
        else:
            for i, response in enumerate(resp.history, 1):
                redirectCount += 1
            if(redirectCount<=1):
                return 0
            elif(redirectCount>=2 and redirectCount<=4):
                return 1
            else:
                return 2 
    
    def rightClickDisabled(self):
        url = self.url_new
            
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        
        driver = webdriver.Chrome(executable_path=r'..\dependencies\windows\chromedriver.exe', options=chrome_options)
        driver.get(url)
        try:
            value = driver.find_element_by_tag_name('body')
            chain = ActionChains(driver)
        except:
            try:
                value = driver.find_element_by_link_text('')
                chain = ActionChains(driver)
            except:
                return 505
        try:
            chain.context_click(value).perform()
            return 0
        except:
            return 1
        driver.quit()
    
    def iFrame(self):
        resp = self.resp
        soup = self.soup
        
        if(resp==696):
            return 696
        elif(resp==707):
            return 707
        else:
            iframe = soup.find_all('iframe')
            
        if(len(iframe)!=0):
            return 1
        else:
            return 0
        
    def ageOfDomain(self):
        w = self.w
        
        if(w==800 ):
            return 800
        elif(w==369 or w==345 or w==469):
            return 1
        else:
            current_time = datetime.now().replace(microsecond=0)
            try:
                if(type(w['creation_date']) == list):
                    days_alive = current_time - w['creation_date'][0]
                else:
                    days_alive = current_time - w['creation_date']
                
                days_alive = int(str(days_alive).split(" ")[0])
                
            except TypeError:
                days_alive = 0
            
            if(days_alive<=180):
                return 1
            else:
                return 0
            
    def dnsRecord(self):
        w = self.w
        
        if(w==800 ):
            return 800
        elif(w==369 or w==345 or w==469):
            return 1
        else:
            if(w!=None):
                return 0
            else:
                return 1
   
    
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