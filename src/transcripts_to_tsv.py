from operator import itemgetter
from os import listdir, makedirs

from scrape_transcript import scrape_transcript
from easy_file_name import easy_file_name

seasons = (1, 2, 3, 4, 5, 6)

episodesOutput = "EPISODE\tSEASON\tFILENAME\n"

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
	
	addedEpisodes = []
	transcriptsForSeason5 = {}
	
	for fileName in fileNames:
		filePath = f"{directory}/{fileName}"
		print(filePath)
		
		with open(filePath, "r", encoding="utf-8") as transcriptFile:
			transcriptHtml = transcriptFile.read()
		
		title, lines = scrape_transcript(transcriptHtml, filePath)
		
		if season != 5:
			outputFileName = easy_file_name(title) +".tsv"
			episodesOutput += f"{title}\t{season}\t{outputFileName}\n"
			linesOutput = "SPEAKER\tLINE\n"
			for line in lines:
				linesOutput += line["SPEAKER"] +"\t"+ line["LINE"] +"\n"
			with open(f"transcripts/initial_tsv/{outputFileName}", "w", encoding="utf-8") as outFile:
				outFile.write(linesOutput.rstrip())
		else:
			titleParts = title.split(" Part ")
			movieTitle = titleParts[0]
			moviePart = titleParts[1]
			outputFileName = easy_file_name(movieTitle) +".tsv"
			
			if movieTitle not in addedEpisodes:
				episodesOutput += f"{movieTitle}\t{season}\t{outputFileName}\n"
				addedEpisodes.append(movieTitle)
				transcriptsForSeason5[movieTitle] = "SPEAKER\tLINE\n"
			
			for line in lines:
				transcriptsForSeason5[movieTitle] += line["SPEAKER"] +"\t"+ line["LINE"] +"\n"
			
			if moviePart == "4":
				with open(f"transcripts/initial_tsv/{outputFileName}", "w", encoding="utf-8") as outFile:
					outFile.write(transcriptsForSeason5[movieTitle].rstrip())

with open("transcripts/initial_tsv/episodes.tsv", "w", encoding="utf-8") as outFile:
	outFile.write(episodesOutput.rstrip())