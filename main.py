import time
import clipboard
textNew = ''
while True:
    text = clipboard.paste()
    if text != textNew:
        textNew = text
        file = open('clip.txt','a')
        file.write(text+"\n") 
        file.close()
    