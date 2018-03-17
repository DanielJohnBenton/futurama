with open("misc_data/stopwords_sql.txt", "r", encoding="utf-8") as inFile:
	content = inFile.read()

content = content.replace("\r\n", " ")

fixed = ""

onSpace = True
for character in content:
	if character == " ":
		if not onSpace:
			fixed +="\n"
			onSpace = True
	else:
		fixed += character
		onSpace = False

fixed = fixed.strip()

with open("misc_data/stopwords.txt", "w", encoding="utf-8") as outFile:
	outFile.write(fixed)

print(fixed)