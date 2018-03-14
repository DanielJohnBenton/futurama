from bs4 import BeautifulSoup

def scrape_transcript(transcriptHtml, fileName):
	soup = BeautifulSoup(transcriptHtml, "html5lib")
	
	[scriptTag.extract() for scriptTag in soup("script")]
	
	h1 = soup.find_all("h1")
	if len(h1) >= 1:
		title = h1[0].text.replace("Transcript:", "").strip()
	
	transcriptHtml = str(soup)
	transcriptHtmlRemovedSquareBrackets = ""
	#print()
	#import sys
	
	squareBracketLevel = 0
	for character in transcriptHtml:
		if character == "[":
			#print()
			#print(f"--- START {squareBracketLevel} ---")
			squareBracketLevel += 1
		elif character == "]" and squareBracketLevel > 0:
			squareBracketLevel -= 1
			#print()
			#print(f"--- END {squareBracketLevel} ---") #remove
		elif squareBracketLevel == 0:
			transcriptHtmlRemovedSquareBrackets += character
		
		#if squareBracketLevel != 0: #remove
			#sys.stdout.write(character) #remove
	
	assert squareBracketLevel == 0, f"Please ensure all square brackets are closed as these blocks need to be removed automatically.\nIn file: {fileName} ({squareBracketLevel})"
	
	transcriptHtml = transcriptHtmlRemovedSquareBrackets
	
	brTags = ("<br />", "<BR />", "<br>", "<BR>")
	for brTag in brTags:
		transcriptHtml = transcriptHtml.replace(f"{brTag}\r\n", " ")
	
	soup = BeautifulSoup(transcriptHtml, "html5lib")
	
	for link in soup.findAll("a"):
		link.unwrap()
	
	transcriptHtml = str(soup)
	
	htmlLines = [line.split("</b>:") for line in transcriptHtml.splitlines() if "</b>:" in line]
	
	lines = []
	for htmlLine in htmlLines:
		lines.append({
			"SPEAKER": htmlLine[0].split("<b>")[-1].replace("\t", " ").strip(),
			"LINE": BeautifulSoup(htmlLine[1], "html5lib").text.replace("\t", " ").strip()
		})
	
	return title, lines