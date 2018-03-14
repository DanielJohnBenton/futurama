from os import listdir, makedirs
from operator import itemgetter
from scrape_transcript import scrape_transcript

seasons = (1, 2, 3, 4, 6)

episodesOutput = ""

for season in seasons:
	directory = f"downloaded_pages/season_{season}"
	fileNames = [fileName for fileName in listdir(directory) if fileName.endswith(".html")]
	
	# sort numerically again because I forgot to left-pad the numbers so the episodes get sorted out of order by listdir:
	fileNamesPieces = []
	for fileName in fileNames:
		pieces = fileName.split("_")
		part1 = int(pieces[0])
		part2 = fileName
		fileNamesPieces.append([part1, part2])
	fileNamesPieces.sort(key=itemgetter(0)) # https://stackoverflow.com/a/4174955
	fileNames = [pieces[1] for pieces in fileNamesPieces]
	
	for fileName in fileNames:
		filePath = f"{directory}/{fileName}"
		print(filePath)
		
		with open(filePath, "r", encoding="utf-8") as transcriptFile:
			transcriptHtml = transcriptFile.read()
		
		title, lines = scrape_transcript(transcriptHtml, filePath)
		
		episodesOutput += f"{title}\t{season}\t{filePath}\n"

print(episodesOutput)