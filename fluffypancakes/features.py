# -*- coding: utf-8 -*-
"""
@authors: Suhas Sharma and Rahul P
"""

from fluffypancakes.handler import Handler
from tqdm import tqdm

class Features:
    def extract_features(self, url, progressBar):
        
        instance = Handler(url)
        
        if progressBar==False:
            if(instance.checkValidURL()==False):
                return ("The URL entered is either Invalid or the Host is unserviceable")
            # Call Functions
            havingAtSymbol = instance.havingAtSymbol()
            doubleSlashRedirection = instance.doubleSlashRedirection()
            havingIPAddress = instance.havingIPAddress()
            lengthOfURL = instance.lengthOfURL()
            shorteningService = instance.shorteningService()
            prefixSuffix = instance.prefixSuffix()
            havingSubDomain = instance.havingSubDomain()
            SSLFinalState = instance.SSLFinalState()
            domainRegistration = instance.domainRegistration()
            faviconCheck = instance.faviconCheck()
            openPorts = instance.openPorts()
            httpsToken = instance.httpsToken()
            requestURL = instance.requestURL()
            urlOfAnchor = instance.urlOfAnchor()
            linksInTags = instance.linksInTags()
            SFH = instance.SFH()
            submittingToMail = instance.submittingToMail()
            abnormalURL = instance.abnormalURL()
            websiteForwarding = instance.websiteForwarding()
            rightClickDisabled = instance.rightClickDisabled()
            iFrame = instance.iFrame()
            ageOfDomain = instance.ageOfDomain()
            dnsRecord = instance.dnsRecord()

        elif progressBar==True:
            
            #Check for Valid URL
            if(instance.checkValidURL()==False):
                return ("The URL entered is either Invalid or the Host is unserviceable")
            
            for i in tqdm(range(1,24), ascii=0, ncols=50, position=0, leave=True):
            # Call Functions
            
                if(i==1):
                    havingAtSymbol = instance.havingAtSymbol()
                if(i==2):
                    doubleSlashRedirection = instance.doubleSlashRedirection()
                if(i==3):
                    havingIPAddress = instance.havingIPAddress()
                if(i==4):
                    lengthOfURL = instance.lengthOfURL()
                if(i==5):
                    shorteningService = instance.shorteningService()
                if(i==6):
                    prefixSuffix = instance.prefixSuffix()
                if(i==7):
                    havingSubDomain = instance.havingSubDomain()
                if(i==8):
                    SSLFinalState = instance.SSLFinalState()
                if(i==9):
                    domainRegistration = instance.domainRegistration()
                if(i==10):
                    faviconCheck = instance.faviconCheck()
                if(i==11):
                    openPorts = instance.openPorts()
                if(i==12):
                    httpsToken = instance.httpsToken()
                if(i==13):
                    requestURL = instance.requestURL()
                if(i==14):
                    urlOfAnchor = instance.urlOfAnchor()
                if(i==15):
                    linksInTags = instance.linksInTags()
                if(i==16):
                    SFH = instance.SFH()
                if(i==17):
                    submittingToMail = instance.submittingToMail()
                if(i==18):
                    abnormalURL = instance.abnormalURL()
                if(i==19):
                    websiteForwarding = instance.websiteForwarding()
                if(i==20):
                    rightClickDisabled = instance.rightClickDisabled()
                if(i==21):
                    iFrame = instance.iFrame()
                if(i==22):
                    ageOfDomain = instance.ageOfDomain()
                if(i==23):
                    dnsRecord = instance.dnsRecord()
                
        
        else:
            return("Enter a valid choice for progressBar. Default option is True")
        
        # Append to the Output Vector
        output_vector = [havingIPAddress, lengthOfURL, shorteningService,
                         havingAtSymbol, doubleSlashRedirection, prefixSuffix, 
                         havingSubDomain, SSLFinalState, domainRegistration, 
                         faviconCheck, openPorts, httpsToken, 
                         requestURL, urlOfAnchor, linksInTags, 
                         SFH, submittingToMail, abnormalURL, 
                         websiteForwarding, rightClickDisabled, iFrame, ageOfDomain, 
                         dnsRecord]
        
        
        return output_vector

