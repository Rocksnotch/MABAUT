from pathlib import Path
import modules.terminalCommandsWindows as terminalCommandsWindows

def writeFileHex(filePayload, filePath):
    rawData = bytes(int(val, 16) for val in filePayload)
    try:
        targetPath = Path(filePath)
        fullPath = targetPath / "content"
        with open(fullPath, "wb") as file:
            file.write(rawData)
        print("Success! File successfully created.")
    except Exception as e:
        print(f"File creation failed. Error: {e}")
    return

def writeFileText(filePayload, filePath):
    rawData = rawData = filePayload.encode('utf-8')
    try:
        targetPath = Path(filePath)
        fullPath = targetPath / "content.txt"
        with open(fullPath, "wb") as file:
            file.write(rawData)
        print("Success! File successfully created.")
    except Exception as e:
        print(f"File creation failed. Error: {e}")
    return

def readFile(filePath):
    # Converted correctly to a path object
    pathObj = Path(filePath)
    binaryString = ""

    try:
        # Open and read
        with open(pathObj, "rb") as file:
            binaryString = "".join(f"{byte:08b}" for byte in file.read())

    except Exception as generalError:
        # Failed to read, either not a file or incorrect
        print(f"File read error occurred: {generalError}")
    
    ETX = '00000011' # ETX(0x03) as binary
    
    EndOfMessageIndex = len(binaryString)
    
    while binaryString[EndOfMessageIndex:EndOfMessageIndex+8] != ETX:
        EndOfMessageIndex -= 8
        
    # Return everything between STX and ETX
    return binaryString[8:EndOfMessageIndex]

def readFolder(folderPath):
    # Convert the path to a path object
    pathObj = Path(folderPath)
    binaryList = []

    # If not a folder, error out
    if not pathObj.is_dir():
        print(f"Error: '{pathObj}' is not a valid directory.")
        return binaryList

    # Go through each file, running the single file read for each
    for file in pathObj.iterdir():
        if file.is_file():
            fileContent = readFile(file)

            if fileContent:
                binaryList.append(fileContent)

    return binaryList