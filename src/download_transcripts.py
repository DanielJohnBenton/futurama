from random import randint
from time import sleep
import urllib.request

from bs4 import BeautifulSoup

# https://stackoverflow.com/a/31857152
# https://stackoverflow.com/a/24226797
def download(url):
	request =  urllib.request.Request(url, data=None, headers={"User-Agent": "Mozilla"})
	response = urllib.request.urlopen(request)
	return response.read().decode("utf-8")

def easy_file_name(text):
	fileName = ""
	for character in text:
		if character.isalpha() or character.isdigit() or character == "_":
			fileName += character
		else:
			fileName +="_"
	return fileName

listPageHtml = download("https://theinfosphere.org/Episode_Transcript_Listing")
listPageSoup = BeautifulSoup(listPageHtml, "html5lib")

# https://stackoverflow.com/a/5815888
links = []
for a in listPageSoup.find_all("a", href=True):
	link = a["href"]
	if "transcript:" in link.lower() and link.lower() not in links:
		if link.startswith("/"):
			link = "https://theinfosphere.org"+ link
		links.append(link)

print(f"{len(links)} links found. Downloading...")

for iLink in range(len(links)):
	sleep(randint(40, 100)) # let's be decent
	link = links[iLink]
	print(link)
	html = download(link)
	fileName = str(iLink + 1) +"_"+ easy_file_name(link.split("/")[-1]) +".html"
	with open(f"downloaded_pages/{fileName}", "w", encoding="utf-8") as newFile:
		newFile.write(html)

print("Done.")