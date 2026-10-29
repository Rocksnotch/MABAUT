import modules.fileHandler as fileHandler
from modules.terminalCommandsWindows import setTopCenter, clearConsole, waitKey

# Global Variables
returnMenu = False

def decodeFile():
    clearConsole()
    setTopCenter()
    print("\n\n\n\n")
    userMessage = input("Enter direct path to file (including file name): ")
    definedPath = input("Enter full path for saving: ")

    binaryData = fileHandler.readFile(userMessage)
    if binaryData == "":
        print("Empty string detected. Exiting.")
        return

    charList = []
    i = 0
    while i + 9 <= len(binaryData):
        chunk = binaryData[i:i + 9]
        if chunk[0] == "0":
            # If it starts with 0, just skip the whole set
            i += 9
        else:
            # Starts with 1
            data_bits = chunk[1:]
            decimalConvert = int(data_bits, 2)
            if 32 <= decimalConvert <= 126:
                # Correct ASCII, store and move forward
                charList.append(chr(decimalConvert))
                i += 9
            else:
                # Invalid ASCII, go the next bit over
                i += 1

    decodedText = "".join(charList)
    fileHandler.writeFileText(decodedText, definedPath)

def decodeFolder():
    return

def beginDecode():
    global returnMenu
    while returnMenu == False:
        clearConsole()
        setTopCenter()
        print("\n\n")
        print("    1) Decode File")
        print("    2) Decode Folder")
        print("    0) Return to Menu")
        print("\n")
        userChoice = input("    Input Requested > ")
        match userChoice:
            case "1":
                decodeFile()
                waitKey()
            case "2":
                decodeFolder()
            case "0":
                print()
                returnMenu = True
            case _:
                print("Unknown entry. ", end="")
                waitKey()