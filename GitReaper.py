import re
import requests
from bs4 import BeautifulSoup
import os
import json

class GitReaper:
    def __init__(self):
        self.github = "https://github.com"
        self.repos = []
        self.emails = []
        self.useTor = False

    def scrapeRepos(self):
        userUrl = f"{self.github}/{self.user}"
        repoUrl = f"{userUrl}?tab=repositories"
        url = repoUrl

        while True:
            if url == "":
                return
            else:
                pass
            req = requests.get(url)
            if req.status_code == 429:
                print("Rate limited, try again later")
                return
            soup = BeautifulSoup(req.text, 'html.parser')

            li = soup.findAll('div', class_="d-inline-block mb-1")
            for _, i in enumerate(li):
                for a in i.findAll('a'):
                    if self.github + a["href"] in self.repos:
                        pass
                    else:
                        if self.user in a['href']:
                            self.repos.append( self.github + a["href"] )

            try:
                req = requests.get(url)
                if req.status_code == 429:
                    print("Rate limited, try again later")
                    return
                soup = BeautifulSoup(req.text, 'html.parser')
                a = soup.findAll('a', class_="btn btn-outline BtnGroup-item")
                nextPage = a[-1]["href"]
                url = nextPage
            except Exception as e:
                nextPage = ""
                url = ""

    def printRepos(self):
        print("###--- REPOS ---###")
        for _, repo in enumerate(self.repos):
            print( _, "\t", repo )
        print("###-------------###")

    def scrapeEmails(self):
        print("Checking commits... this might take a while")
        git = "https://github.com"
        for _, repoUrl in enumerate(self.repos):
            url = repoUrl
            lastUrl = ""
            print(url)
            pages = 0
            while True:
                if url == "":
                    break
                elif lastUrl == url:
                    print("Url repeated twise - stopping -- lasturl: " + lastUrl)
                    break
                else:
                    pages += 1
                commitsUrl = repoUrl + "/commits"
                req = requests.get(commitsUrl)
                soup = BeautifulSoup(req.text, "html.parser")

                div = soup.findAll('div', class_="d-none d-md-block flex-shrink-0")
                for _, btnGroup in enumerate(div):
                    commitId = btnGroup.findAll('a', class_="tooltipped tooltipped-sw btn-outline btn BtnGroup-item text-mono f6")
                    commitId = commitId[0]["href"]
                    req = requests.get(git + commitId + ".patch")
                    if req.status_code == 429:
                        print("Rate limited, try again later")
                        return
                    email = re.findall(r"From: .*", req.text)
                    try:
                        if email[0] in self.emails:
                            pass
                        else:
                            self.emails.append(email[0])
                    except:
                        # No email
                        pass
                    
                try:
                    req = requests.get(url)
                    if req.status_code == 429:
                        print("Rate limited, try again later")
                        return
                    soup = BeautifulSoup(req.text, 'html.parser')
                    a = soup.findAll('a', class_="btn btn-outline BtnGroup-item")
                    for _, btn in enumerate(a):
                        if "Older" in btn:
                            nextPage = btn["href"]
                    if nextPage == None:
                        return
                    lastUrl = url
                    url = nextPage
                except Exception as e:
                    nextPage = ""
                    lastUrl = url
                    url = ""
            print(f"Pages: {pages}")

    def printEmails(self):
        print("###--- EMAILS ---###")
        for _, email in enumerate(self.emails):
            print(_, "\t", email)
        print("###--------------###")

    def setUser(self, user):
        self.user = user
