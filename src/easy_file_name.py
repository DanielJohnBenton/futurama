def easy_file_name(text):
	fileName = ""
	for character in text:
		if character.isalpha() or character.isdigit() or character == "_":
			fileName += character
		else:
			fileName +="_"
	return fileName