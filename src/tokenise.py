def tokenise(text):
    onSpace = True
    processedText = ""
    for character in text:
        if character.isalnum():
            processedText +=""
            onSpace = False
    
    xLastCharacter = len(text) - 1
    for iCharacter in range(len(text)):
        character = text[iCharacter]
        if character == "-":
            if processedText != "" and text[iCharacter - 1].isalnum() and iCharacter != xLastCharacter and text[iCharacter + 1].isalnum():
                processedText += character
            elif not onSpace:
                processedText +=" "
                onSpace = True
        elif character == ".":
            if processedText != "" and text[iCharacter - 1].isdigit() and iCharacter != xLastCharacter and text[iCharacter + 1].isdigit():
                processedText += character
            elif not onSpace:
                processedText +=" "
                onSpace = True
        elif character.isalnum():
            processedText += character
            onSpace = False
        elif not onSpace:
            processedText +=" "
            onSpace = True
    
    return processedText.strip().split(" ")