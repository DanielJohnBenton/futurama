from os import listdir
from scrape_transcript import scrape_transcript

seasons = (1, 2, 3, 4, 5, 6)

for season in seasons:
	directory = f"downloaded_pages/season_{season}"
	fileNames = [fileName for fileName in listdir(directory) if fileName.endswith(".html")]
	for fileName in fileNames:
		#if "beast" not in fileName.lower():
			#continue
		filePath = f"{directory}/{fileName}"
		print(filePath)
		
		with open(filePath, "r", encoding="utf-8") as transcriptFile:
			transcriptHtml = transcriptFile.read()
		
		title, lines = scrape_transcript(transcriptHtml, filePath)